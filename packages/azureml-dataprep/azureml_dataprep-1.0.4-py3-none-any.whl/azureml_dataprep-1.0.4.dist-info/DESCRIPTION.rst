# Azure Machine Learning Data Prep SDK

The Azure Machine Learning Data Prep SDK is used to load, transform, and write data for machine learning workflows.
You can interact with the SDK in any Python environment, including Jupyter Notebooks or your favorite Python IDE.
The Azure Machine Learning Data Prep SDK includes the following functionality to help prepare your data for modeling:

- *Intelligent transforms*. Use the SDK to [derive](https://docs.microsoft.com/en-us/python/api/azureml-dataprep/azureml.dataprep.api.builders.derivecolumnbyexamplebuilder?view=azure-dataprep-py) or [split](https://docs.microsoft.com/en-us/python/api/azureml-dataprep/azureml.dataprep.api.builders.splitcolumnbyexamplebuilder?view=azure-dataprep-py) a column by example, [impute](https://docs.microsoft.com/en-us/python/api/azureml-dataprep/azureml.dataprep.api.builders.imputemissingvaluesbuilder?view=azure-dataprep-py) missing values, [fuzzy group](https://docs.microsoft.com/en-us/python/api/azureml-dataprep/azureml.dataprep.api.builders.fuzzygroupbuilder?view=azure-dataprep-py), [auto join](https://docs.microsoft.com/en-us/python/api/azureml-dataprep/azureml.dataprep.api.builders.joinbuilder?view=azure-dataprep-py), and perform other automated tasks.
- *Auto reading functionality*. The SDK can automatically detect any of the supported file types. You don’t need to use special file readers for CSV, text, Excel, etc., or to specify delimiter, header, or encoding parameters.
- *Varying schema processing*. The SDK engine can read different columns per row instance, also sometimes referred to as ragged-right format.
- *Scale through streaming*. Instead of loading all the data into memory, the SDK engine serves data using streaming, allowing it to scale and perform better on large datasets.
- *Cross-platform functionality* with a single code artifact. Write to a single SDK and run it on Windows, macOS, Linux, or Spark in a scale-up or scale-out manner. When running in scale-up, the engine attempts to utilize all hardware threads available, when running scale-out the engine allows the distributed scheduler to optimize execution.

## Install the SDK

To install the Azure Machine Learning Data Prep SDK for Python, use the following command:

```bash
pip install --upgrade azureml-dataprep
```

## Learn how to use it

Here are some resources to help you learn more about the Azure Machine Learning Data Prep SDK for Python:

- See the Azure Machine Learning service documentation to learn how to [load, transform, and write data with the SDK](https://docs.microsoft.com/azure/machine-learning/service/how-to-data-prep).
- Review an [example notebook in GitHub](https://github.com/Microsoft/PendletonDocs/blob/master/Scenarios/GettingStarted/getting-started.ipynb) of data preparation using the SDK.
- Use the [API Reference](https://docs.microsoft.com/en-us/python/api/azureml-dataprep/?view=azure-dataprep-py) to look up classes and modules.


