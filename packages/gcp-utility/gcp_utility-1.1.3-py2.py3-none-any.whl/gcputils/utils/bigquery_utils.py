from google.cloud import bigquery
import logging
import time


class BigQueryUtils:

    def __init__(self, project=None, credentials=None, _http=None):
        """

        :param project:
        :param credentials:
        :param _http:
        """
        self.project = project
        self.credentials = credentials
        self._http = _http

    # return bigqurery connection object
    def get_connection(self, service_account_file_path=None):
        """

        :param service_account_file_path:
        :return:
        """
        return bigquery.Client.from_service_account_json(json_credentials_path=service_account_file_path, project=self.project) \
            if service_account_file_path \
            else bigquery.Client(project=self.project, credentials=self.credentials, _http=self._http)

    def export_data_to_gcs(self, bq_client, dataset_id, table_id, destination):
        """

        :param bq_client: bigquery client object
        :param dataset_id: string
        :param table_id: string
        :param destination: gcs uri string
        :return:
        """
        dataset_ref = bq_client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)
        job_config = bigquery.job.ExtractJobConfig()

        job_config.print_header = False
        job = bq_client.extract_table(table_ref, destination, job_config=job_config)

        while job.state != 'DONE':
            time.sleep(10)
            logging.info("job status %s", job.state)  # Waits for job to complete

    def query_to_table(self,
                       bq_client,
                       query,
                       dest_dataset_id,
                       dest_table_id,
                       flattern_results=True,
                       write_disposition='WRITE_TRUNCATE',
                       create_disposition = 'CREATE_IF_NEEDED',
                       time_partitioning = None,
                       time_partitioning_field = None,
                       clustering_fields = None,
                       use_standard_sql=False):
        """

        :param bq_client:
        :param query:
        :param dest_dataset_id:
        :param dest_table_id:
        :param flattern_results:
        :param write_disposition:
        :param create_disposition:
        :param time_partitioning:
        :param time_partitioning_field:
        :param clustering_fields: list
        :param use_standard_sql:
        :return:
        """
        try:
            client = bq_client
            job_config = bigquery.QueryJobConfig()
            logging.info("destination table id - {}".format(dest_table_id))
            logging.info("destination dataset id - {}".format(dest_dataset_id))

            # Allow for query results larger than the maximum response size.
            job_config.allow_large_results = True

            # When large results are allowed, a destination table must be set.
            dest_dataset_ref = client.dataset(dest_dataset_id)
            dest_table_ref = dest_dataset_ref.table(dest_table_id)
            #table = bigquery.Table(dest_table_ref)
            job_config.destination = dest_table_ref
            #job_config.flatten_results = flattern_results
            # Allow the results table to be overwritten.
            job_config.write_disposition = write_disposition
            job_config.create_disposition = create_disposition

            if time_partitioning is not None:
                job_config.time_partitioning = bigquery.table.TimePartitioning(type_=time_partitioning, field=time_partitioning_field)
                job_config.clustering_fields = clustering_fields.split(',') if clustering_fields is not None else None

            job_config.use_legacy_sql = True
            if use_standard_sql:
                job_config.use_legacy_sql = False
            query_job = client.query(query, job_config=job_config)
            logging.info("job status %s", query_job.state)

            for row in query_job.result():  # Waits for job to complete.
                #logging.info(row)
                logging.info("job status %s", query_job.state)
                if query_job.state == 'DONE':
                    break
            logging.info("Job completed successfully")
        except Exception, e:
            logging.info(e)
            logging.info("please create date partition table before loading datainto it")
            logging.info("bq mk --time_partitioning_type=DAY dataset.table")
            raise Exception(e)







