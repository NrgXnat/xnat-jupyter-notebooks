# xnat-jupyter-notebooks

This repository currently contains sample notebooks for use in the XNAT/Jupyter integrated environment. Head to [xnat-docker-compose/features/jupyterhub](https://github.com/NrgXnat/xnat-docker-compose/tree/features/jupyterhub) for information on setting that up.

You will also find notebooks used for the Jupyter demonstration during the XNAT Workshop in London 2022.

## Getting Started

After you **Start Jupyter** from XNAT, start a terminal from within JupyterLab.

Your workspace directory is available at **/workspace/{username}**.

```shell
cd $JUPYTERHUB_ROOT_DIR
```

This is where you should store any Jupyter notebooks. **Notebooks stored here will persist between Jupyter sessions**. Git repositories should also be stored here. 

```shell
git clone https://github.com/NrgXnat/xnat-jupyter-notebooks.git
```

After cloning checkout the sample notebook for a overview of the XNAT/Jupyter environmental variables, naviagting the XNAT file system, and converting stored searches to pandas DataFrames. There is also a introductory MONAI image classification tutorial using the MedNIST dataset.
