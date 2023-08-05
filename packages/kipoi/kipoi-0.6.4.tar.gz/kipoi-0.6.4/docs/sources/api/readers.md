#kipoi.readers

Readers useful for creating new dataloaders

- HDF5Reader

##HDF5Reader

```python
HDF5Reader(self, file_path)
```
Read the HDF5 file. Convenience wrapper around h5py.File

__Arguments__

- __file_path__: File path to an HDF5 file

###ls

```python
HDF5Reader.ls(self)
```
Recursively list the arrays

###load_all

```python
HDF5Reader.load_all(self, unflatten=True)
```
Load the whole file

__Arguments__

- __unflatten__: if True, nest/unflatten the keys.
      e.g. an entry `f['/foo/bar']` would need to be accessed
- __using two nested `get` call__: `f['foo']['bar']`

###batch_iter

```python
HDF5Reader.batch_iter(self, batch_size=16, **kwargs)
```
Create a batch iterator over the whole file

__Arguments__

- __batch_size__: batch size
- __**kwargs__: ignored argument. Used for consistency with other dataloaders

###open

```python
HDF5Reader.open(self)
```
Open the file

###close

```python
HDF5Reader.close(self)
```
Close the file

###load

```python
HDF5Reader.load(file_path, unflatten=True)
```
Load the data all at once (classmethod).

__Arguments__

- __file_path__: HDF5 file path
- __unflatten__: see `load_all`

