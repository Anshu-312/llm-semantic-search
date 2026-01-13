import faiss

def flat_index(dim: int):
    # Exact search (baseline)
    """Creates a FAISS flat (brute-force) index.

    Args:
        dim (int): The dimensionality of the vectors to be indexed.

    Returns:
        faiss.IndexFlatIP: A FAISS flat index instance.
    """
    return faiss.IndexFlatIP(dim)

def ivf_index(dim : int, nlist: int = 100):
    # Inverted File Index
    """Creates a FAISS Inverted File (IVF) index.

    Args:
        dim (int): The dimensionality of the vectors to be indexed.
        nlist (int, optional): The number of clusters to use in the IVF index. Defaults to 100.

    Returns:
        faiss.IndexIVFFlat: A FAISS IVF index instance.
    """
    quantizer = faiss.IndexFlatIP(dim)
    index = faiss.IndexIVFFlat(quantizer, dim, nlist, faiss.METRIC_INNER_PRODUCT)
    return index

def hnsw_index(dim : int, m: int = 32):
    # Hierarchical Navigable Small World Graph
    """Creates a FAISS HNSW index.

    Args:
        dim (int): The dimensionality of the vectors to be indexed.
        m (int, optional): The number of bi-directional links created for each new element during construction. Defaults to 32.

    Returns:
        faiss.IndexHNSWFlat: A FAISS HNSW index instance.
    """
    index = faiss.IndexHNSWFlat(dim, m, faiss.METRIC_INNER_PRODUCT)
    return index