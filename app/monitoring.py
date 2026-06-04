import datetime as dt

## Create an empty dict with pipeline metrics

pipeline_metrics = {
    'run_timestamp': dt.datetime.now(),
    'number_of_records_input': 0,
    'number_of_records_output': 0,
    'number_of_records_dropped': 0,
    'number_of_books': 0,
    'number_of_customers': 0,
    'pipeline_execution_time': 0,
}