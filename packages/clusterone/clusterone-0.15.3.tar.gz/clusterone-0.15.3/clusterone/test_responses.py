# coding: utf-8

TEST_INSTANCES = [{
                      'slug': 'c5.2xlarge', 'name': 'c5.2xlarge', 'type': 'c5.2xlarge', 'type_class': 'c', 'cpu': 8,
                      'memory': 30, 'gpu': 0, 'description': '', 'show_for_ps': True, 'show_for_workers': True,
                      'blessed': True, 'queue': 'job-master-queue', 'cudann': None
                  }, {
                      'slug': 'c5.4xlarge', 'name': 'c5.4xlarge', 'type': 'c5.4xlarge', 'type_class': 'c', 'cpu': 16,
                      'memory': 30, 'gpu': 0, 'description': '', 'show_for_ps': True, 'show_for_workers': True,
                      'blessed': True, 'queue': 'job-master-queue', 'cudann': None
                  }, {
                      'slug': 'c5.8xlarge', 'name': 'c5.8xlarge', 'type': 'c5.8xlarge', 'type_class': 'c', 'cpu': 1,
                      'memory': 2, 'gpu': 0, 'description': '', 'show_for_ps': True, 'show_for_workers': True,
                      'blessed': True, 'queue': 'job-master-queue', 'cudann': None
                  }, {
                      'slug': 'c5.xlarge', 'name': 'c5.xlarge', 'type': 'c5.xlarge', 'type_class': 'c', 'cpu': 4,
                      'memory': 7, 'gpu': 0, 'description': '', 'show_for_ps': True, 'show_for_workers': True,
                      'blessed': True, 'queue': 'job-master-queue', 'cudann': None
                  }, {
                      'slug': 'p2.8xlarge', 'name': 'p2.8xlarge', 'type': 'p2.8xlarge', 'type_class': 'p', 'cpu': 32,
                      'memory': 488, 'gpu': 8, 'description': '', 'show_for_ps': True, 'show_for_workers': True,
                      'blessed': True, 'queue': 'job-master-queue', 'cudann': 8.0
                  }, {
                      'slug': 'p2.xlarge', 'name': 'p2.xlarge', 'type': 'p2.xlarge', 'type_class': 'p', 'cpu': 4,
                      'memory': 61, 'gpu': 1, 'description': '', 'show_for_ps': True, 'show_for_workers': True,
                      'blessed': True, 'queue': 'job-master-queue', 'cudann': 8.0
                  }, {
                      'slug': 'p3.2xlarge', 'name': 'p3.2xlarge', 'type': 'p3.2xlarge', 'type_class': 'p', 'cpu': 8,
                      'memory': 61, 'gpu': 1, 'description': '', 'show_for_ps': True, 'show_for_workers': True,
                      'blessed': True, 'queue': 'job-master-queue', 'cudann': 9.2
                  }, {
                      'slug': 'p3.8xlarge', 'name': 'p3.8xlarge', 'type': 'p3.8xlarge', 'type_class': 'p', 'cpu': 32,
                      'memory': 244, 'gpu': 4, 'description': '', 'show_for_ps': True, 'show_for_workers': True,
                      'blessed': True, 'queue': 'job-master-queue', 'cudann': 9.2
                  }, {
                      'slug': 't2.2xlarge', 'name': 't2.2xlarge', 'type': 't2.2xlarge', 'type_class': 'c', 'cpu': 1,
                      'memory': 2, 'gpu': 0, 'description': '', 'show_for_ps': True, 'show_for_workers': True,
                      'blessed': True, 'queue': 'job-master-queue', 'cudann': None
                  }, {
                      'slug': 't2.large', 'name': 't2.large', 'type': 't2.large', 'type_class': 'c', 'cpu': 2,
                      'memory': 8, 'gpu': 0, 'description': '', 'show_for_ps': True, 'show_for_workers': True,
                      'blessed': True, 'queue': 'job-master-queue', 'cudann': None
                  }, {
                      'slug': 't2.medium', 'name': 't2.medium', 'type': 't2.medium', 'type_class': 'c', 'cpu': 2,
                      'memory': 4, 'gpu': 0, 'description': '', 'show_for_ps': True, 'show_for_workers': True,
                      'blessed': True, 'queue': 'job-master-queue', 'cudann': None
                  }, {
                      'slug': 't2.small', 'name': 't2.small', 'type': 't2.small', 'type_class': 'c', 'cpu': 1,
                      'memory': 2, 'gpu': 0, 'description': '', 'show_for_ps': True, 'show_for_workers': True,
                      'blessed': True, 'queue': 'job-master-queue', 'cudann': None
                  }, {
                      'slug': 't2.xlarge', 'name': 't2.xlarge', 'type': 't2.xlarge', 'type_class': 'c', 'cpu': 1,
                      'memory': 2, 'gpu': 0, 'description': '', 'show_for_ps': True, 'show_for_workers': True,
                      'blessed': True, 'queue': 'job-master-queue', 'cudann': None
                  }]

TEST_DOCKER_IMAGES = [{
    'slug': 'juliagpu-1.0.0-gpu-cuda9.2', 'name': 'julia', 'version': '1.0.0', 'description': '',
    'docker_image_path': 'quay.io/clusteronecom/juliagpu:1.0.0-gpu-cuda9.2',
    'imagepull_secrets': 'clusteronecom-deploy-ml-pull-secret'
}, {
    'slug': 'pytorch-0.4.0-gpu-py36-cuda9.2', 'name': 'pytorch', 'version': '0.4.0', 'description': '',
    'docker_image_path': 'quay.io/clusteronecom/pytorch:0.5.0-gpu-py36-cuda9.2',
    'imagepull_secrets': 'clusteronecom-deploy-ml-pull-secret'
}, {
    'slug': 'tensorflow-1.4.0-gpu-py27-cuda9.0', 'name': 'tensorflow', 'version': '1.4.0',
    'description': '', 'docker_image_path': 'quay.io/clusteronecom/tensorflow:1.4.0-gpu-py27-cuda9.0',
    'imagepull_secrets': 'clusteronecom-deploy-ml-pull-secret'
}, {
    'slug': 'tensorflow-1.3.0-gpu-py27-cuda9.0', 'name': 'tensorflow', 'version': '1.3.0',
    'description': '', 'docker_image_path': 'quay.io/clusteronecom/tensorflow:1.3.0-gpu-py27-cuda9.0',
    'imagepull_secrets': 'clusteronecom-deploy-ml-pull-secret'
}, {
    'slug': 'tensorflow-1.3.0-cpu-py36', 'name': 'tensorflow', 'version': '1.3.0', 'description': '',
    'docker_image_path': 'quay.io/clusteronecom/tensorflow:1.3.0-cpu-py36',
    'imagepull_secrets': 'clusteronecom-deploy-ml-pull-secret'
}, {
    'slug': 'tensorflow-1.8.0-cpu-py36', 'name': 'tensorflow', 'version': '1.8.0', 'description': '',
    'docker_image_path': 'quay.io/clusteronecom/tensorflow:1.8.0-cpu-py36',
    'imagepull_secrets': 'clusteronecom-deploy-ml-pull-secret'
}, {
    'slug': 'tensorflow-1.8.0-gpu-py36-cuda9.2', 'name': 'tensorflow', 'version': '1.8.0',
    'description': '', 'docker_image_path': 'quay.io/clusteronecom/tensorflow:1.8.0-gpu-py36-cuda9.2',
    'imagepull_secrets': 'clusteronecom-deploy-ml-pull-secret'
}, {
    'slug': 'tensorflow-1.9.0-cpu-py36', 'name': 'tensorflow', 'version': '1.9.0', 'description': '',
    'docker_image_path': 'quay.io/clusteronecom/tensorflow:1.9.0-cpu-py36',
    'imagepull_secrets': 'clusteronecom-deploy-ml-pull-secret'
}, {
    'slug': 'tensorflow-1.4.0-gpu-py36-cuda9.0', 'name': 'tensorflow', 'version': '1.4.0',
    'description': '', 'docker_image_path': 'quay.io/clusteronecom/tensorflow:1.4.0-gpu-py36-cuda9.0',
    'imagepull_secrets': 'clusteronecom-deploy-ml-pull-secret'
}]
