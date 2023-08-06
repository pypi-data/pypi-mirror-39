from .base import CSEndpoint
from tenable.errors import InvalidInputError
from io import BytesIO

class ReportsAPI(CSEndpoint):
    def report(self, container_id=None, image_id=None, digest=None):
        '''
        Retrieves the image report by the image digest.

        Args:
            digest (str): The image digest.

        Returns:
            dict: The report resource record.
        '''
        return self._api.get('v2/reports/{}'.format(
            self._check('digest', digest, str))).json()

    def nessus_report(self, container_id, fobj=None):
        '''
        `container-security-reports: nessus-report-by-container-id <https://cloud.tenable.com/api#/resources/container-security-reports/nessus-report-by-container-id>`_

        Args:
            container_id (int): The unique identifier for the container image.
            fobj (FileObject, optional): 
                The file-like object to write the Nessus report into.  If none
                is specified, then we will use a BytesIO object to write the
                Nessus report into.

        Returns:
            FileObject: The Nessus report file.
        '''
        resp = self._api.get('v1/reports/nessus/show', params={
            'id': self._check('container_id', container_id, int)})

        # If no file object was given to us, then lets create a new BytesIO
        # object to dump the data into.
        if not fobj:
            fobj = BytesIO()

        # Stream the data into the file.
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)

        # return the FileObject.
        return fobj
