# Orthanc REST client

Provides a REST client, based on [apiron](https://github.com/ithaka/apiron), targeted at [Orthanc](https://www.orthanc-server.com) REST endpoints.

### How to use

Import the pre-defined client and pass the server details

    from orthanc_rest_client import Orthanc
    orthanc = Orthanc(scheme='http', domain='localhost', port=8042)

    # Get list of patients
    orthanc.patients()

There are other preconfigured endpoints.

For further help:
- [apiron](https://github.com/ithaka/apiron)
- [Orthanc](https://www.orthanc-server.com)
