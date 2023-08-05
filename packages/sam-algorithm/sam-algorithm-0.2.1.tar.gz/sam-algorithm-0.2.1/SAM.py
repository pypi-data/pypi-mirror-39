import time
from sklearn.preprocessing import Normalizer
import pickle
import pandas as pd
import utilities as ut
import sklearn.manifold as man
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
import numpy as np

try:
    import matplotlib.pyplot as plt
    PLOTTING = True
except ImportError:
    print('matplotlib not installed. Plotting functions disabled')
    PLOTTING = False


__version__ = '0.2.1'

"""
Copyright 2018, Alexander J. Tarashansky, All rights reserved.
Email: <tarashan@stanford.edu>
"""


"""
TODO: Line-by-line documentation.
"""


class SAM(object):
    """Self-Assembling Manifolds single-cell RNA sequencing analysis tool.

    SAM iteratively rescales the input gene expression matrix to emphasize
    that are spatially variable along the intrinsic manifold of the data.
    It outputs the gene weights, nearest neighbor matrix, distance matrix, and
    a 2D projection.

    Parameters
    ----------
    counts : pandas.DataFrame, optional, default None
        A DataFrame of the gene expression counts (cells x genes).

    annotations : numpy.ndarray, optional, default None
        A Numpy array of cell annotations.

    k : int, optional, default None
        The number of nearest neighbors to identify for each cell. If
        None, k will be automatically be set to the square root of
        the number of cells in the dataset.

    distance : string, optional, default 'correlation'
        The distance metric to use when constructing cell distance
        matrices. Can be any of the distance metrics supported by
        sklearn's 'pdist'.

    Attributes
    ----------
    dataset : pandas.DataFrame
        Unfiltered raw expression counts (cells x genes)

    ann : numpy.ndarray
        Cell annotations (optional).

    k: int
        The number of nearest neighbors to identify for each cell
        when constructing the nearest neighbor graph.

    distance: str
        The distance metric used when constructing the cell-to-cell
        distance matrix.

    filtered_dataset: pandas.DataFrame
        The filtered data (cells x genes).

    num_expressed_genes: numpy.ndarray
        The number of expressed genes in each cell.

    D: numpy.ndarray
        The numpy array version of 'filtered_dataset' (equivalent to
        filtered_dataset.values).

    gene_names: numpy.ndarray
        A vector of the gene names (equivalent to filtered_dataset.columns).

    cell_names: numpy.ndarray
        A vector of the cell names (equivalent to filtered_dataset.index).

    annotations: numpy.ndarray
        A vector of cell annotations if they were provided.

    integer_annotations: numpy.ndarray
        A vector of cell annotations converted to integers.

    D_avg: numpy.ndarray
        The k-nearest-neighbor-averaged expression data.

    weighted_data: numpy.ndarray
        The rescaled expression data.

    D_sub: numpy.ndarray
        If the 'n_genes' parameter is set, D_sub is the subsetted gene
        expression matrix. Otherwise, it is equal to 'D'.

    weighted_sub: numpy.ndarray
        If the 'n_genes' parameter is set, weighted_sub is the subsetted
        weighted expression matrix. Otherwise, it is equal to 'weighted_data'.

    wPCA_data: numpy.ndarray
        The weighted PCA matrix.

    pca: sklearn.decomposition.PCA
        The sklearn pca object.

    dist: numpy.ndarray
        The cell-to-cell distance matrix.

    indices: numpy.ndarray
        Indices sorting the genes according to the weights in descending order
        (i.e. indices[0] is the index of the gene with the largest weight).

    nnm_adj: numpy.ndarray
        The nearest neighbor adjacency matrix.

    weights: numpy.ndarray
        A vector of weights for each gene.

    ranked_genes: numpy.ndarray
        The ranked list of genes, i.e. sam.gene_names[sam.indices].

    dt: numpy.ndarray
        The t-SNE embedding.

    gene_groups: list of numpy.ndarray
        Each element of the list contains a vector of gene indices that are
        correlated with each other.

    geneID_groups: list of numpy.ndarray
        Each element of the list contains a vector of gene IDs that are
        correlated with each other.

    """

    def __init__(self, counts=None, annotations=None, k=None,
                 distance='correlation'):
        self.dataset = counts
        self.annotations = annotations

        if(self.annotations is not None):
            self.integer_annotations = ut.convert_annotations(self.annotations)

        if(self.dataset is not None):
            self.filtered_dataset = self.remove_zero_columns(self.dataset)
            self.log_transform(self.filtered_dataset)
            self.load_attributes_from_data(self.filtered_dataset)

        self.k = k
        self.distance = distance
        self.analysis_performed = False

        self.output_vars = {}

    def load_data_from_file(self, filename, do_filtering=True, transpose=True,
                            sep=',', **kwargs):
        """Reads the specified tabular data file and stores the data in a
        Pandas DataFrame.

        This is a wrapper function that loads the file specified by 'filename'
        and filters the data.

        Parameters
        ----------
        filename - string
            The path to the tabular raw expression counts file.

        sep - string, optional, default ','
            The delimeter used to read the input data table. By default
            assumes the input table is delimited by commas.

        do_filtering - bool, optional, default True
            If True, filters the data with default parameters using
            'filter_data'. Otherwise, loads the data without filtering
            (aside from removing genes with no expression at all).

        transpose - bool, optional, default True
            By default, assumes file is (genes x cells). Set this to False if
            the file has dimensions (cells x genes).

        Keyword arguments
        -----------------

        div : float, default 1
            The factor by which the gene expression will be divided prior to
            log normalization.

        downsample : float, default 0
            The factor by which to randomly downsample the data. If 0, the data
            will not be downsampled.

        genes : array-like of string or int, default None
            A vector of gene names or indices that specifies the genes to keep.
            All other genes will be filtered out. If specified, the usual
            filtering operations do not occur. Gene names are case-sensitive.

        cells : array-like of string or int, default None
            A vector of cell names or indices that specifies the cells to keep.
            All other cells wil lbe filtered out. Cell names are
            case-sensitive.

        min_expression : float, default 1
            The threshold (in log2 TPM) above which a gene is considered
            expressed. Gene expression values less than 'min_expression' are
            set to zero.

        thresh : float, default 0.2
            Keep genes expressed in greater than 'thresh'*100 % of cells and
            less than (1-'thresh')*100 % of cells, where a gene is considered
            expressed if its expression value exceeds 'min_expression'.

        filter_genes : bool, default True
            A convenience parameter. Setting this to False turns off all
            filtering operations.

        """
        df = pd.read_csv(filename, sep=sep, index_col=0)
        if(transpose):
            self.dataset = df.T
        else:
            self.dataset = df

        if(do_filtering):
            self.filter_data(**kwargs)
        else:
            self.filtered_dataset = self.remove_zero_columns(self.dataset)
            self.log_transform(self.filtered_dataset)
            self.load_attributes_from_data(self.filtered_dataset)

    def remove_zero_columns(self, data):
        return data.iloc[:, data.values.sum(0) > 0].astype('float')

    def load_attributes_from_data(self, data):
        self.D = data.values.copy()
        self.gene_names = np.array(list(data.columns.values))
        self.cell_names = np.array(list(data.index.values))

    def log_transform(self, data, in_place=True):
        if(in_place):
            np.add(data.values, 1, out=data.values)
            np.log2(data.values, out=data.values)
        else:
            return np.log2(data+1)

    def filter_data(self, div=1, downsample=0, genes=None, cells=None,
                    min_expression=1, thresh=0.02, filter_genes=True):
        """Log-normalizes and filters the expression data.

        Parameters
        ----------

        div : float, optional, default 1
            The factor by which the gene expression will be divided prior to
            log normalization.

        downsample : float, optional, default 0
            The factor by which to randomly downsample the data. If 0, the
            data will not be downsampled.

        genes : array-like of string or int, optional, default None
            A vector of gene names or indices that specifies the genes to keep.
            All other genes will be filtered out. If specified, the usual
            filtering operations do not occur. Gene names are case-sensitive.

        cells : array-like of string or int, optional, default None
            A vector of cell names or indices that specifies the cells to keep.
            All other cells wil lbe filtered out. Cell names are
            case-sensitive.

        min_expression : float, optional, default 1
            The threshold (in log2 TPM) above which a gene is considered
            expressed. Gene expression values less than 'min_expression' are
            set to zero.

        thresh : float, optional, default 0.2
            Keep genes expressed in greater than 'thresh'*100 % of cells and
            less than (1-'thresh')*100 % of cells, where a gene is considered
            expressed if its expression value exceeds 'min_expression'.

        filter_genes : bool, optional, default True
            A convenience parameter. Setting this to False turns off all
            filtering operations.

        """
        if(self.dataset is None):
            print('No data loaded')
            return
        self.filtered_dataset = self.log_transform(
            self.dataset/div, in_place=False)

        if(genes is not None):
            genes = np.array(genes)

            if str(genes.dtype)[:2] == '<U' or str(genes.dtype) == 'object':
                idx = np.where(
                    (np.in1d(self.filtered_dataset.columns.values, genes)))[0]
            else:
                idx = genes

            self.filtered_dataset = self.filtered_dataset.iloc[:, idx]

            filter_genes = False

        if(cells is not None):
            cells = np.array(cells)
            if str(cells.dtype)[:2] == '<U' or str(cells.dtype) == 'object':
                idx2 = np.where(
                    np.in1d(self.filtered_dataset.index.values, cells))[0]
            else:
                idx2 = cells

            self.filtered_dataset = self.filtered_dataset.iloc[idx2, :]

        if downsample > 0:
            numcells = int(self.filtered_dataset.shape[0]/downsample)
            self.filtered_dataset = self.filtered_dataset.iloc[
                np.random.choice(np.arange(self.filtered_dataset.shape[0]),
                                 size=numcells, replace=False), :]

        else:
            numcells = self.filtered_dataset.shape[0]

        temp_data = np.array(self.filtered_dataset)

        temp_data[temp_data <= min_expression] = 0
        temp_data[temp_data > 0] = 1

        self.num_expressed_genes = temp_data.sum(1)

        if(filter_genes):
            keep = np.where(np.logical_and(np.sum(temp_data, axis=0)/numcells
                                           > thresh, np.sum(temp_data, axis=0)/numcells <=
                                           1-thresh))[0]
        else:
            keep = np.where(temp_data.sum(0) > 0)[0]

        self.filtered_dataset = self.filtered_dataset.iloc[:, keep]
        self.filtered_dataset[self.filtered_dataset <= min_expression] = 0

        self.load_attributes_from_data(self.filtered_dataset)

    def load_annotations(self, aname):
        """Loads cell annotations.

        Loads the cell annoations specified by the 'aname' path.

        """
        ann = pd.read_csv(aname, header=None)
        if(ann.size != self.dataset.shape[0]):
            ann = pd.read_csv(aname, index_col=0, header=None)
        if(ann.size != self.dataset.shape[0]):
            ann = pd.read_csv(aname, index_col=0)
        if(ann.size != self.dataset.shape[0]):
            ann = pd.read_csv(aname)

        if(ann.size != self.filtered_dataset.shape[0]):
            ann = ann.values.flatten()[np.where(
                np.in1d(self.dataset.index.values,
                        self.filtered_dataset.index.values))[0]]
        else:
            ann = ann.values.flatten()

        self.annotations = ann
        self.integer_annotations = ut.convert_annotations(self.annotations)

    def dispersion_ranking_NN(self, dist, num_norm_avg=50):
        """Computes the spatial dispersion factors for each gene.

        Given a cell distance matrix, this function calculates the k-nearest
        neighbor adjacency matrix, and performs k-nearest-neighbor averaging
        of the expression data. From the averaged expression data, the Fano
        factor (variance/mean) for each gene is computed. These factors are
        square rooted and then min-max normalized to generate the
        gene weights, from which gene rankings are calculated.


        Loads the cell annoations specified by 'ann_name' during the creation
        of the SAM object.

        Parameters
        ----------
        dist - ndarray, float
            Square cell-to-cell distance matrix.

        num_norm_avg - int, optional, default 50
            The top 'num_norm_avg' dispersions are averaged to determine the
            normalization factor when calculating the weights.

        Returns:
        -------
        indices - ndarray, int
            The indices corresponding to the gene weights sorted in decreasing
            order.

        weights - ndarray, float
            The vector of gene weights.

        nnm - ndarray, int
            The square k-nearest-neighbor directed adjacency matrix.

        D_avg - ndarray, float
            The k-nearest-neighbor-averaged expression data.

        """
        nnm = ut.dist_to_nn(dist, self.k)

        D_avg = nnm.dot(self.D)/np.sum(nnm, axis=1).reshape(self.D.shape[0], 1)

        dispersions = D_avg.var(0)/D_avg.mean(0)
        ma = np.sort(dispersions)[-num_norm_avg:].mean()
        dispersions[dispersions >= ma] = ma

        weights = ut.normalizer(dispersions**0.5)

        indices = np.argsort(-weights)

        self.D_avg = D_avg

        return indices, weights, nnm, D_avg

    def louvain_clustering(self, res=1):
        if (not self.analysis_performed):
            print("Please run the SAM analysis first using 'run' after "
                  "loading the data.")
        else:
            import anndata
            import scanpy.api as sc
            adata = anndata.AnnData(self.D, var={'genes': self.gene_names},
                                    obs={'cells': self.cell_names})
            adata.obsm['X_pca'] = self.wPCA_data
            sc.pp.neighbors(adata, n_neighbors=self.k, metric='correlation',
                            method='umap')
            sc.tl.louvain(adata, resolution=res)
            self.cluster_labels = adata.obs['louvain'].values.astype('int')
            self.output_vars['louvain_cluster_labels'] = self.cluster_labels

    def identify_marker_genes(self, n_genes_per_cluster=10, labels=None,
                              n_genes_subset=2000, svm=True):
        if(labels is None):
            try:
                lbls = self.cluster_labels
            except AttributeError:
                print("Please generate cluster labels first or set the "
                      "'labels' keyword argument.")
                return
        else:
            lbls = labels

        if(not svm):
            import sklearn.linear_model
            obj = sklearn.linear_model.LogisticRegression(
                solver='liblinear', multi_class='auto')
        else:
            import sklearn.svm
            obj = sklearn.svm.LinearSVC()

        rawD = self.dataset[list(self.ranked_genes[:n_genes_subset])]
        obj.fit(rawD.values, lbls)
        idx = np.argsort(-(obj.coef_), axis=1)

        markers = np.zeros(
            (idx.shape[0], n_genes_per_cluster), dtype=self.gene_names.dtype)
        for i in range(idx.shape[0]):
            markers[i, :] = rawD.columns[idx[i, :n_genes_per_cluster]]

        self.marker_genes = markers
        self.output_vars['marker_genes'] = self.marker_genes

    def run(self,
            max_iter=15,
            stopping_condition=1e-5,
            verbose=True,
            projection=None,
            n_genes=2000,
            npcs=150,
            num_norm_avg=50,
            weight_PCs=True):
        """Runs the Self-Assembling Manifold algorithm.

        Parameters
        ----------
        max_iter - int, optional, default 15
            The maximum number of iterations SAM will run.

        stopping_condition - float, optional, default 1e-4
            The convergence threshold for the error between adjacent cell
            distance matrices.

        verbose - bool, optional, default True
            If True, the iteration number and convergence score will be
            displayed.

        projection - str, optional, default None
            If 'tsne', generates a t-SNE embedding. If 'umap', generates a UMAP
            embedding. Otherwise, no embedding will be generated.

        npcs - int, optional, default None
            Determines the number of weighted principal
            components to take. If None, all principal components will be
            selected. For large datasets (>5000 cells), we recommend 'npcs' to
            be lowered (e.g. npcs = 500) if runtime is an issue. Otherwise,
            selecting all principal components should be fine.

        n_genes - int, optional, default None
            Improve runtime by selecting only the top 'n_genes' weighted genes
            when computing PCA. If None, use all genes.

        num_norm_avg - int, optional, default 50
            The top 'num_norm_avg' dispersions are averaged to determine the
            normalization factor when calculating the weights.
        """
        if(not self.k):
            self.k = int(self.D.shape[0]**0.5)

        if(self.k < 5):
            self.k = 5
        elif(self.k > 100):
            self.k = 100

        if(n_genes is not None):
            if(n_genes < 2*num_norm_avg):
                n_genes = 2*num_norm_avg

        if(self.k > self.D.shape[0]-1):
            print("Warning: chosen k exceeds the number of cells")
            self.k = self.D.shape[0]-2

        print('RUNNING SAM')

        numcells = self.D.shape[0]
        tinit = time.time()

        dist = np.random.rand(numcells, numcells)*2
        dist[np.arange(numcells), np.arange(numcells)] = 0

        _, dispersions, edm, _ = self.dispersion_ranking_NN(
            dist, num_norm_avg=num_norm_avg)

        W = dispersions.reshape((1, self.D.shape[1]))

        old = dist

        new = np.random.rand(numcells, numcells)*2
        new[np.arange(numcells), np.arange(numcells)] = 0

        i = 0

        err = ut.distance_matrix_error(new, old)
        while (err > stopping_condition and i < max_iter):

            conv = err
            if(verbose):
                print('Iteration: ' + str(i) + ', Convergence: ' + str(conv))

            i += 1
            old = new
            if(n_genes is None):
                gkeep = np.arange(W.size)
            else:
                gkeep = np.sort(np.argsort(-W.flatten())[:n_genes])

            weighted_data = self.D*W.flatten()[None, :]
            self.weighted_data = weighted_data
            self.D_sub = self.D[:, gkeep]
            self.weighted_sub = self.weighted_data[:, gkeep]
            g_weighted, pca = ut.weighted_PCA(
                Normalizer().fit_transform(self.weighted_sub),
                do_weight=weight_PCs, npcs=npcs)

            self.wPCA_data = g_weighted
            self.pca = pca

            dist = ut.compute_distances(g_weighted, self.distance)
            idx2, dispersions, EDM, _ = self.dispersion_ranking_NN(
                dist, num_norm_avg=num_norm_avg)

            W = dispersions.reshape((1, self.D.shape[1]))

            self.dist = dist
            self.indices = idx2.flatten()
            self.nnm_adj = EDM
            self.weights = W.flatten()
            new = dist
            err = ut.distance_matrix_error(new, old)

        self.ranked_genes = self.gene_names[self.indices]

        self.output_vars['distance_matrix'] = self.dist
        self.output_vars['ranked_gene_indices'] = self.indices
        self.output_vars['ranked_gene_names'] = self.ranked_genes
        self.output_vars['nearest_neighbor_matrix'] = self.nnm_adj
        self.output_vars['gene_weights'] = self.weights

        self.analysis_performed = True

        if(projection is 'tsne'):
            print('Computing the t-SNE embedding...')
            self.run_tsne()
        elif(projection is 'umap'):
            print('Computing the UMAP embedding...')
            self.run_umap()

        self.corr_bin_genes(number_of_features=2000)

        elapsed = time.time()-tinit

        print('Elapsed time: ' + str(elapsed) + ' seconds')

    def save(self, savename, dirname=None, exc=None):
        """Saves all SAM attributes to a Pickle file.

        Saves all SAM attributes to a Pickle file which can be later loaded
        into an empty SAM object.

        Parameters
        ----------
        savename - string
            The name of the pickle file (not including the file extension) to
            write to.

        dirname - string, optional, default None
            The path/name of the directory in which the Pickle file will be
            saved. If None, the file will be saved to the current working
            directory.

        exc - array-like of strings, optional, default None
            A vector of SAM attributes to exclude from the saved file.
        """
        self._create_dict(exc)

        if(dirname is not None):
            ut.create_folder(dirname+"/")
            f = open(dirname+"/" + savename + ".p", 'wb')
        else:
            f = open(savename + ".p", 'wb')

        pickle.dump(self.pickle_dict, f)
        f.close()

    def load(self, n):
        """Loads SAM attributes from a Pickle file.

        Loads all SAM attributes from the specified Pickle file into the SAM
        object.

        Parameters
        ----------
        n - string
            The path of the Pickle file.
        """
        f = open(n, 'rb')
        pick_dict = pickle.load(f)
        for i in range(len(pick_dict)):
            self.__dict__[list(pick_dict.keys())[i]
                          ] = pick_dict[list(pick_dict.keys())[i]]
        f.close()

    def _create_dict(self, exc):
        self.pickle_dict = self.__dict__.copy()
        if(exc):
            for i in range(len(exc)):
                try:
                    del self.pickle_dict[exc[i]]
                except NameError:
                    0  # do nothing

    def plot_top_genes(self, n_genes=5, **kwargs):
        """Plots expression patterns of the top ranked genes.

        Parameters
        ----------
        n_genes - int, optional, default 5
            The number of top ranked genes to display.

        **kwargs -
            All keyword arguments in 'show_gene_expression' and 'scatter'
            are eligible.
        """
        for i in range(n_genes):
            self.show_gene_expression(self.indices[i], **kwargs)

    def save_marker_genes_to_pdf(self, filename, **kwargs):
        nclusts = self.cluster_labels.max()+1
        lbls = np.tile(np.arange(nclusts)[
                       :, None], (1, self.marker_genes.shape[1]))
        lbls = lbls.flatten()
        lbls_colors = np.zeros_like(self.cluster_labels)

        try:
            plt.ioff()
            for i, gene in enumerate(self.marker_genes.flatten()):
                lbls_colors[:] = 0
                lbls_colors[self.cluster_labels == lbls[i]] = 1
                plt.figure(figsize=(12, 5))
                ax1 = plt.subplot(121)
                self.show_gene_expression(gene, axes=ax1, **kwargs)
                ax2 = plt.subplot(122)
                self.scatter(c=lbls_colors, colorbar=False, axes=ax2, **kwargs)
                plt.set_cmap('rainbow')
                plt.title('Cluster: ' + str(lbls[i]))

            self.save_figures(filename)
            plt.close('all')
            plt.ion()

        except AttributeError:
            print("Please run 'identify_marker_genes' first.")

    def save_figures(self, filename, fig_IDs=None, **kwargs):

        if(fig_IDs is not None):
            if(type(fig_IDs) is list):
                savetype = 'pdf'
            else:
                savetype = 'png'
        else:
            savetype = 'pdf'

        if(savetype == 'pdf'):
            from matplotlib.backends.backend_pdf import PdfPages

            if(len(filename.split('.')) == 1):
                filename = filename + '.pdf'
            else:
                filename = '.'.join(filename.split('.')[:-1])+'.pdf'

            pdf = PdfPages(filename)

            if fig_IDs is None:
                figs = [plt.figure(n) for n in plt.get_fignums()]
            else:
                figs = [plt.figure(n) for n in fig_IDs]

            for fig in figs:
                fig.savefig(pdf, format='pdf', **kwargs)
            pdf.close()
        elif(savetype == 'png'):
            plt.figure(fig_IDs).savefig(filename, **kwargs)

    def plot_correlated_groups(self, group=None, n_genes=5, **kwargs):
        """Plots orthogonal expression patterns.

        In the default mode, plots orthogonal gene expression patterns. A
        specific correlated group of genes can be specified to plot gene
        expression patterns within that group.

        Parameters
        ----------
        group - int, optional, default None
            If specified, display the genes within the desired correlated
            group. Otherwise, display the top ranked gene within each distinct
            correlated group.

        n_genes - int, optional, default 5
            The number of top ranked genes to display within a correlated
            group if 'group' is specified.

        **kwargs -
            All keyword arguments in 'show_gene_expression' and 'scatter'
            are eligible.
        """
        self.corr_bin_genes(number_of_features=2000)

        if(group is None):
            for i in range(len(self.gene_groups)):
                self.show_gene_expression(self.gene_groups[i][0], **kwargs)
        else:
            for i in range(n_genes):
                self.show_gene_expression(self.gene_groups[group][i], **kwargs)

    def plot_correlated_genes(self, name, n_genes=5, **kwargs):
        """Plots gene expression patterns correlated with the input gene.

        Parameters
        ----------
        name - string
            The name of the gene with respect to which correlated gene
            expression patterns will be displayed.

        n_genes - int, optional, default 5
            The number of top ranked correlated genes to display.

        average_exp - bool, optional, default True
            If True, the plots use the k-nearest-neighbor-averaged expression
            values to smooth out noisy expression patterns and improves
            visualization.

        **kwargs -
            All keyword arguments in 'show_gene_expression' and 'scatter'
            are eligible.
        """
        name = np.where(self.gene_names == name)[0]
        if(name.size == 0):
            print(
                "Gene note found in the filtered dataset. Note that genes "
                "are case sensitive.")
            return
        sds, _ = self.corr_bin_genes(input_gene=name, number_of_features=2000)

        for i in range(1, n_genes+1):
            self.show_gene_expression(sds[0][i], **kwargs)
        return self.gene_names[sds[0][1:]]

    def corr_bin_genes(self, number_of_features=None, input_gene=None):
        """A (hacky) method for binning groups of correlated genes.

        """
        if (not self.analysis_performed):
            print("Please run the SAM analysis first using 'run' after loading"
                  " the data.")
        else:

            idx2 = np.argsort(-self.weights)

            if(number_of_features is None or number_of_features > idx2.size):
                number_of_features = idx2.size

            if(input_gene is not None):
                if(type(input_gene) is str):
                    input_gene = np.where(self.gene_names == input_gene)[0]
                    if(input_gene.size == 0):
                        print(
                            "Gene note found in the filtered dataset. Note "
                            "that genes are case sensitive.")
                        return
                seeds = [np.array([input_gene])]
                pw_corr = np.corrcoef(
                    self.D_avg[:, idx2[:number_of_features]].T)
                for i in range(1, number_of_features):
                    flag = False
                    maxd = np.mean(pw_corr[i, :][pw_corr[i, :] > 0])
                    maxi = 0
                    for j in range(len(seeds)):
                        if(pw_corr[np.where(idx2 == seeds[j][0])[0], i]
                           > maxd):
                            maxd = pw_corr[np.where(idx2 == seeds[j][0])[0], i]
                            maxi = j
                            flag = True
                    if(not flag):
                        seeds.append(np.array([idx2[i]]))
                    else:
                        seeds[maxi] = np.append(seeds[maxi], idx2[i])

                geneID_groups = []
                for i in range(len(seeds)):
                    geneID_groups.append(self.gene_names[seeds[i]])

                return seeds, geneID_groups
            else:
                seeds = [np.array([idx2[0]])]
                pw_corr = np.corrcoef(
                    self.D_avg[:, idx2[:number_of_features]].T)
                for i in range(1, number_of_features):
                    flag = False
                    maxd = np.mean(pw_corr[i, :][pw_corr[i, :] > 0])
                    maxi = 0
                    for j in range(len(seeds)):
                        if(pw_corr[np.where(idx2 == seeds[j][0])[0], i]
                           > maxd):
                            maxd = pw_corr[np.where(idx2 == seeds[j][0])[0], i]
                            maxi = j
                            flag = True
                    if(not flag):
                        seeds.append(np.array([idx2[i]]))
                    else:
                        seeds[maxi] = np.append(seeds[maxi], idx2[i])

                self.gene_groups = seeds
                self.geneID_groups = []
                for i in range(len(self.gene_groups)):
                    self.geneID_groups.append(
                        self.gene_names[self.gene_groups[i]])

                return seeds
    
    def run_tsne(self, X=None, metric='precomputed',**kwargs):
        """Wrapper for sklearn's t-SNE implementation.

        See sklearn for the t-SNE documentation. All arguments are the same
        with the exception that 'metric' is set to 'precomputed' by default,
        implying that this function expects a distance matrix by default.
        """
        if(X is not None):
            dt = man.TSNE(metric=metric,**kwargs).fit_transform(X)
            self.tsne2d = dt
            return self.tsne2d.copy()
        
        elif(not self.analysis_performed):
            print("Please run the SAM analysis first using 'run' after "
                  "loading the data.")
        
        else:
            dt = man.TSNE(metric=metric,**kwargs).fit_transform(self.dist)
            self.tsne2d = dt
            self.output_vars['tsne_projection'] = self.tsne2d        
            return self.tsne2d.copy()
    
    def run_umap(self, X=None, metric=None, **kwargs):
        """Wrapper for umap-learn.

        See https://github.com/lmcinnes/umap sklearn for the documentation
        and source code.
        """

        import umap as umap

        if metric is None:
            metric = self.distance
        
        if(X is not None):
            umap_obj = umap.UMAP(metric=metric, **kwargs)
            self.umap2d = umap_obj.fit_transform(X)            
            return self.umap2d.copy()
        
        elif (not self.analysis_performed):
            print("Please run the SAM analysis first using 'run' after "
                  "loading the data.")
        else:
            umap_obj = umap.UMAP(metric=metric, **kwargs)
            self.umap2d = umap_obj.fit_transform(self.wPCA_data)
            self.output_vars['umap_projection'] = self.umap2d        
            return self.umap2d.copy()
        
    def scatter(self, projection=None, c=None, cmap='rainbow', axes=None,
                colorbar=True, **kwargs):
        """Display a scatter plot.

        Displays a scatter plot using the SAM projection or another input
        projection with or without annotations.

        Parameters
        ----------

        projection - ndarray of floats, optional, default None
            An N x 2 matrix, where N is the number of data points. If None,
            use an existing SAM projection (default t-SNE). Can take on values
            'umap' or 'tsne' to specify either the SAM UMAP embedding or
            SAM t-SNE embedding.

        c - ndarray, optional, default None
            Colors for each cell in the scatter plot. Can be a vectory of
            floats or strings for cell annotations.

        cmap - string, optional, default 'rainbow'
            The colormap to use for the input color values.

        new_figure - bool, optional, default True
            If True, creates a new figure. Otherwise, outputs the scatter plot
            to currently active matplotlib axes.

        colorbar - bool, optional default True
            If True, display a colorbar indicating which values / annotations
            correspond to which color in the scatter plot.

        Keyword arguments -
            All other keyword arguments that can be passed into
            matplotlib.pyplot.scatter can be used.
        """
        if (not self.analysis_performed and projection is None):
            print("Please run the SAM analysis first using 'run' after loading"
                  " the data.")
        elif (not PLOTTING):
            print("matplotlib not installed!")
        else:
            if(projection is 'umap'):
                try:
                    dt = self.umap2d
                except AttributeError:
                    print('Please create a UMAP projection first.')
                    return
            elif(projection is 'tsne'):
                try:
                    dt = self.tsne2d
                except AttributeError:
                    print('Please create a t-SNE projection first.')
                    return
            elif(projection is None):
                try:
                    dt = self.tsne2d
                except AttributeError:
                    try:
                        dt = self.umap2d
                    except AttributeError:
                        print("Please create either a t-SNE or UMAP projection"
                              "first.")
                        return
            else:
                dt = projection

            if(axes is None):
                plt.figure()
                axes = plt.gca()

            if(c is None):
                plt.scatter(dt[:, 0], dt[:, 1], **kwargs)
            else:
                if((type(c[0]) is str or type(c[0]) is np.str_) and
                   (type(c) is np.ndarray or type(c) is list)):
                    i = ut.convert_annotations(c)
                    ui, ai = np.unique(i, return_index=True)
                    cax = axes.scatter(
                        dt[:, 0], dt[:, 1], c=i, cmap=cmap, **kwargs)

                    if(colorbar):
                        cbar = plt.colorbar(cax, ticks=ui)
                        cbar.ax.set_yticklabels(c[ai])
                else:
                    if not (type(c) is np.ndarray or type(c) is list):
                        colorbar = False
                    i = c

                    cax = axes.scatter(
                        dt[:, 0], dt[:, 1], c=i, cmap=cmap, **kwargs)

                    if(colorbar):
                        plt.colorbar(cax)

    def show_gene_expression(self, gene, average_exp=True, **kwargs):
        """Display a gene's expressions.

        Displays a scatter plot using the SAM projection or another input
        projection with a particular gene's expressions overlaid.

        Parameters
        ----------
        gene - string or int
            a case-sensitive string indicating the gene expression pattern
            to display or the integer corresponding to the gene's column index
            in the filtered dataset.

        average_exp - bool, optional, default True
            If True, the plots use the k-nearest-neighbor-averaged expression
            values to smooth out noisy expression patterns and improves
            visualization.

        **kwargs - keyword arguments in 'scatter' are eligible

        """

        if(type(gene) == str or type(gene) == np.str_):
            idx = np.where(self.gene_names == gene)[0]
            name = gene
            if(idx.size == 0):
                print(
                    "Gene note found in the filtered dataset. Note that genes "
                    "are case sensitive.")
                return
        else:
            idx = gene
            name = self.gene_names[idx]

        if(average_exp):
            a = self.D_avg[:, idx].flatten()
        else:
            a = self.D[:, idx].flatten()

        self.scatter(c=a, **kwargs)
        plt.title(name)
