"""
Tools for saving, loading, and converting PETSc matrices and vectors on file
"""
import logging
from petsc4py import PETSc
from mpi4py import MPI

try:
    import PetscBinaryIO
except BaseException:
    print(("Could not import PetscBinaryIO. Please set PYTHONPATH so we can "
           "find it. Typically it's found in $PETSC_DIR/lib/petsc/bin."))
    exit(1)

def symmetrize(MAT : PETSc.Mat):
    """
    Symmetrizes a matrix. This can be used to get rid of slight unsymmetricity
    due to numerical inaccuracies.

    Parameters
    ----------
    MAT : petsc4py.PETSc.Mat
        Matrix to symmetrize

    Returns
    -------
    ½ (MAT+MAT^T)
    """
    if not MAT.isSymmetric(tol=1e-8):
        logging.warning(("Matrix "+MAT.name+" is not close to symmetric, but attempting"
                        " to symmetrize it"))

    MAT_trans = PETSc.Mat()
    MAT.transpose(MAT_trans)
    return 0.5*(MAT+MAT_trans)

def antisymmetrize(MAT : PETSc.Mat):
    """
    Antisymmetrizes a matrices. Can be used to get rid of slight 
    numerical errors.

    Parameters
    ----------
    MAT : petsc4py.PETSc.Mat
        The matrix to antisymmetrize

    Returns
    -------
    ½ ( MAT - MAT^T)
    """
    MAT_trans = PETSc.Mat()
    MAT.transpose(MAT_trans)
    return 0.5*(MAT-MAT_trans)


def petsc_vecload(path: str, comm: MPI.Comm) -> PETSc.Vec:
    """Loads a PETSc vector saved in the PETSc binary format."""
    viewer = PETSc.Viewer().createBinary(name=path, mode='r', comm=comm)
    return PETSc.Vec().load(viewer)


def petsc_matload(path: str, comm: MPI.Comm) -> PETSc.Mat:
    """Loads a PETSc matrix saved in the PETSc binary format."""
    viewer = PETSc.Viewer().createBinary(name=path, mode='r', comm=comm)
    return PETSc.Mat().load(viewer)


def petsc_save(name: str, obj, comm: MPI.Comm) -> None:
    """Saves a PETSc vector or matrix in the PETSc binary format"""
    viewer = PETSc.Viewer().createBinary(name, mode='w',
                                         comm=comm)
    if isinstance(obj, PETSc.Mat):
        if obj.type in [PETSc.Mat.Type.DENSE, PETSc.Mat.Type.SEQDENSE,
                        PETSc.Mat.Type.MPIDENSE]:
            viewer.pushFormat(PETSc.Viewer.Format.NATIVE)
    viewer(obj)


def petsc_convert_to_complex(name: str) -> None:
    """Converts a PETSc binary savefile from real type to complex type"""
    io = PetscBinaryIO.PetscBinaryIO()
    io.complexscalars = False
    io._update_dtypes()

    mat, = io.readBinaryFile(name, mattype='sparse')

    io.complexscalars = True
    io._update_dtypes()

    io.writeBinaryFile(name + "_cplx", [mat, ])


def petsc_convert_to_real(name: str) -> None:
    """Converts of a PETSc binary savefile from complex type to real type"""
    io = PetscBinaryIO.PetscBinaryIO()
    io.complexscalars = True
    io._update_dtypes()

    mat, = io.readBinaryFile(name, mattype='sparse')

    io.complexscalars = False
    io._update_dtypes()

    io.writeBinaryFile(name + "_real", [mat, ])
