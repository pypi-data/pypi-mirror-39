# LabelOps
Operates on labeled neuronal meshes.

- Compresses and decompresses neuron cell part labels based on the boundaries of those labels.

# Installation
```
git clone https://github.com/cajal/LabelOps.git
cd LabelOps
pip3 install .
```

# Usage
```
from labelops import LabelOps as op

# Assuming mesh data already stored in variables: vertices and triangles
# Assuming label data already stored in variable: vertex_labels

# Compress labels
neighborhood = op.generate_neighborhood(triangles)
compressed_labels = op.compress_labels(neighborhood, vertex_labels, as_dict=False)

# Decompress labels into 2D array with vertex indices in first column and labels in second column
decompressed_labels = op.decompress_labels(neighborhood, compressed_labels, as_dict=False)

# Reconstruct labels as a flat array, same format as vertex labels
reconstructed_labels = op.reconstruct_labels(neighborhood, compressed_labels, len(vertices))

# Retrieve labels for specified vertex indices from compressed labels
target_node_labels = op.decompress_targets(target_nodes, neighborhood, compressed_labels)
```
