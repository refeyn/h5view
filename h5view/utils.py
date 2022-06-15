from typing import Any, Mapping, Tuple, Union

import h5py
import numpy as np


def formatAsStr(value: Any) -> str:
    if isinstance(value, h5py.Group):
        return f"Group {value.name!r} with {len(value.keys())} members"
    elif isinstance(value, h5py.Dataset):
        if value.shape == ():
            singlevalue = value[()]
            if isinstance(singlevalue, bytes):
                try:
                    return singlevalue.decode()
                except ValueError:
                    pass
            return str(singlevalue)
        else:
            return (
                f"Dataset {value.name!r} {typeAndShapeAsStr(value.dtype, value.shape)}"
            )
    elif isinstance(value, bytes):
        try:
            return value.decode()
        except ValueError:
            return str(value)
    else:
        return str(value)


def typeAsStr(dtype: np.dtype) -> str:
    if h5py.check_string_dtype(dtype):
        return "string"
    elif h5py.check_vlen_dtype(dtype):
        return f"vlen array of {typeAsStr(h5py.check_vlen_dtype(dtype))}"
    elif h5py.check_enum_dtype(dtype):
        return "enum"
    elif dtype == h5py.ref_dtype:
        return "object reference"
    elif dtype == h5py.regionref_dtype:
        return "region reference"
    else:
        return str(dtype)


def typeAndShapeAsStr(dtype: np.dtype, shape: Tuple[int, ...]) -> str:
    if shape == ():
        return typeAsStr(dtype)
    else:
        return f"{typeAsStr(dtype)}{shape}"


def metadataFor(obj: Union[h5py.Group, h5py.Dataset]) -> Mapping[str, Any]:
    if isinstance(obj, h5py.Group):
        return {}
    else:
        return {
            "Shape": obj.shape,
            "DType": obj.dtype,
            "NBytes": obj.nbytes,
            "Max shape": obj.maxshape,
            "Chunk shape": obj.chunks,
            "Compression": obj.compression,
            "Compression opts": obj.compression_opts,
        }
