# Performance Output Parameters types
TYPE_DEFAULT = 'DEFAULT'
TYPE_TRAINED_MODEL = 'TRAINED_MODEL'
TYPE_RESULT_MATRIX = 'RESULT_MATRIX'
TYPE_ANALYSIS_RESULT = 'ANALYSIS_RESULT'
TYPE_RESULT_DATASET = 'RESULT_DATASET'

# Analysis types
ANALYSIS_TYPE_BATCH = 'batch'
ANALYSIS_TYPE_ITERATIVE = 'iterative'

# Datasets
DEMO_INPUT_DATASET = {
    'id': 'aid',
    'datasource_id': 'psql_data_source_input',
    'table': 'records',
    'schema': {
        'fields': [
            {
                'name': 'id',
                'type': 'int'
            },
            {
                'name': 'name',
                'type': 'string'
            }
        ]
    }
}

DEMO_OUTPUT_DATASET = {
    "id": "output_dataset",
    'datasource_id': 'psql_data_source_output',
    "table": "records_output",
    "schema": {
        "fields": [
            {
                "name": "id",
                "type": "int"
            },
            {
                "name": "name",
                "type": "string"
            }
        ]
    }
}
