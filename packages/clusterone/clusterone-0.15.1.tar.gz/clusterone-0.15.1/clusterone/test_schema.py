# coding: utf-8

TEST_API_SCHEMA = {
  "_type": "document",
  "_meta": {
    "url": "http://localhost:8000/",
    "title": "Clusterone API"
  },
  "add_git_webhook": {
    "read": {
      "_type": "link",
      "url": "/api/add_git_webhook/{username}/{name}/",
      "action": "get",
      "description": "This view handles adding a gitlab_api commits to JSON commit field when someone pushes a commit\n:param request:\n:param name:\n:return:",
      "fields": [
        {
          "name": "name",
          "required": True,
          "location": "path"
        },
        {
          "name": "username",
          "required": True,
          "location": "path"
        }
      ]
    },
    "create": {
      "_type": "link",
      "url": "/api/add_git_webhook/{username}/{name}/",
      "action": "post",
      "description": "This view handles adding a gitlab_api commits to JSON commit field when someone pushes a commit\n:param request:\n:param name:\n:return:",
      "fields": [
        {
          "name": "name",
          "required": True,
          "location": "path"
        },
        {
          "name": "username",
          "required": True,
          "location": "path"
        }
      ]
    }
  },
  "auth": {
    "tensorboard": {
      "list": {
        "_type": "link",
        "url": "/api/auth/tensorboard/",
        "action": "get"
      }
    }
  },
  "charge": {
    "create": {
      "_type": "link",
      "url": "/api/charge/",
      "action": "post"
    }
  },
  "datasets": {
    "details": {
      "read": {
        "_type": "link",
        "url": "/api/datasets/details/{username}/{name}/",
        "action": "get",
        "description": "Updates, Removes an existing dataset.",
        "fields": [
          {
            "name": "name",
            "required": True,
            "location": "path"
          },
          {
            "name": "username",
            "required": True,
            "location": "path"
          }
        ]
      },
      "update": {
        "_type": "link",
        "url": "/api/datasets/details/{username}/{name}/",
        "action": "put",
        "encoding": "application/json",
        "description": "Updates, Removes an existing dataset.",
        "fields": [
          {
            "name": "name",
            "required": True,
            "location": "path"
          },
          {
            "name": "username",
            "required": True,
            "location": "path"
          },
          {
            "name": "bucket_name",
            "location": "form"
          },
          {
            "name": "icon",
            "location": "form"
          },
          {
            "name": "color",
            "location": "form"
          },
          {
            "name": "name",
            "required": True,
            "location": "form"
          },
          {
            "name": "source",
            "location": "form"
          },
          {
            "name": "full_name",
            "location": "form"
          },
          {
            "name": "parameters",
            "location": "form"
          },
          {
            "name": "description",
            "location": "form"
          },
          {
            "name": "http_url_to_repo",
            "location": "form"
          },
          {
            "name": "parent_repository",
            "location": "form"
          },
          {
            "name": "is_public",
            "location": "form"
          },
          {
            "name": "tags",
            "location": "form"
          },
          {
            "name": "repository_username",
            "location": "form"
          },
          {
            "name": "repository_token",
            "location": "form"
          }
        ]
      },
      "partial_update": {
        "_type": "link",
        "url": "/api/datasets/details/{username}/{name}/",
        "action": "patch",
        "encoding": "application/json",
        "description": "Updates, Removes an existing dataset.",
        "fields": [
          {
            "name": "name",
            "required": True,
            "location": "path"
          },
          {
            "name": "username",
            "required": True,
            "location": "path"
          },
          {
            "name": "bucket_name",
            "location": "form"
          },
          {
            "name": "icon",
            "location": "form"
          },
          {
            "name": "color",
            "location": "form"
          },
          {
            "name": "name",
            "location": "form"
          },
          {
            "name": "source",
            "location": "form"
          },
          {
            "name": "full_name",
            "location": "form"
          },
          {
            "name": "parameters",
            "location": "form"
          },
          {
            "name": "description",
            "location": "form"
          },
          {
            "name": "http_url_to_repo",
            "location": "form"
          },
          {
            "name": "parent_repository",
            "location": "form"
          },
          {
            "name": "is_public",
            "location": "form"
          },
          {
            "name": "tags",
            "location": "form"
          },
          {
            "name": "repository_username",
            "location": "form"
          },
          {
            "name": "repository_token",
            "location": "form"
          }
        ]
      },
      "delete": {
        "_type": "link",
        "url": "/api/datasets/details/{username}/{name}/",
        "action": "delete",
        "description": "Updates, Removes an existing dataset.",
        "fields": [
          {
            "name": "name",
            "required": True,
            "location": "path"
          },
          {
            "name": "username",
            "required": True,
            "location": "path"
          }
        ]
      }
    },
    "link": {
      "create": {
        "_type": "link",
        "url": "/api/datasets/link/",
        "action": "post",
        "encoding": "application/json",
        "fields": [
          {
            "name": "name",
            "required": True,
            "location": "form"
          },
          {
            "name": "full_name",
            "location": "form"
          },
          {
            "name": "description",
            "location": "form"
          },
          {
            "name": "http_url_to_repo",
            "location": "form"
          },
          {
            "name": "parent_repository",
            "location": "form"
          },
          {
            "name": "tags",
            "location": "form"
          },
          {
            "name": "source",
            "location": "form"
          },
          {
            "name": "repository_username",
            "location": "form"
          },
          {
            "name": "repository_token",
            "location": "form"
          }
        ]
      }
    },
    "members": {
      "expire": {
        "list": {
          "_type": "link",
          "url": "/api/datasets/{username}/{name}/members/{member_username}/expire/",
          "action": "get",
          "fields": [
            {
              "name": "name",
              "required": True,
              "location": "path"
            },
            {
              "name": "username",
              "required": True,
              "location": "path"
            },
            {
              "name": "member_username",
              "required": True,
              "location": "path"
            }
          ]
        }
      },
      "list": {
        "_type": "link",
        "url": "/api/datasets/{username}/{name}/members/",
        "action": "get",
        "description": "ListAPIView returns :model:'projects.RepositoryMembership' model based on dataset",
        "fields": [
          {
            "name": "name",
            "required": True,
            "location": "path"
          },
          {
            "name": "username",
            "required": True,
            "location": "path"
          },
          {
            "name": "limit",
            "location": "query"
          },
          {
            "name": "offset",
            "location": "query"
          }
        ]
      }
    },
    "new": {
      "create": {
        "_type": "link",
        "url": "/api/datasets/new/",
        "action": "post",
        "encoding": "application/json",
        "fields": [
          {
            "name": "name",
            "required": True,
            "location": "form"
          },
          {
            "name": "full_name",
            "location": "form"
          },
          {
            "name": "description",
            "location": "form"
          },
          {
            "name": "http_url_to_repo",
            "location": "form"
          },
          {
            "name": "parent_repository",
            "location": "form"
          },
          {
            "name": "tags",
            "location": "form"
          },
          {
            "name": "source",
            "location": "form"
          },
          {
            "name": "repository_username",
            "location": "form"
          },
          {
            "name": "repository_token",
            "location": "form"
          }
        ]
      }
    },
    "owned": {
      "list": {
        "_type": "link",
        "url": "/api/datasets/owned/",
        "action": "get",
        "description": "Get a list of datasets which are owned by the authenticated user.",
        "fields": [
          {
            "name": "page",
            "location": "query"
          },
          {
            "name": "limit",
            "location": "query"
          },
          {
            "name": "search",
            "location": "query"
          },
          {
            "name": "name",
            "location": "query"
          },
          {
            "name": "description",
            "location": "query"
          },
          {
            "name": "http_url_to_repo",
            "location": "query"
          },
          {
            "name": "created_at",
            "location": "query"
          },
          {
            "name": "owner",
            "location": "query"
          },
          {
            "name": "modified_at",
            "location": "query"
          }
        ]
      },
      "create": {
        "_type": "link",
        "url": "/api/datasets/owned/",
        "action": "post",
        "encoding": "application/json",
        "description": "Get a list of datasets which are owned by the authenticated user.",
        "fields": [
          {
            "name": "bucket_name",
            "location": "form"
          },
          {
            "name": "icon",
            "location": "form"
          },
          {
            "name": "color",
            "location": "form"
          },
          {
            "name": "name",
            "required": True,
            "location": "form"
          },
          {
            "name": "source",
            "location": "form"
          },
          {
            "name": "full_name",
            "location": "form"
          },
          {
            "name": "parameters",
            "location": "form"
          },
          {
            "name": "description",
            "location": "form"
          },
          {
            "name": "http_url_to_repo",
            "location": "form"
          },
          {
            "name": "parent_repository",
            "location": "form"
          },
          {
            "name": "is_public",
            "location": "form"
          },
          {
            "name": "tags",
            "location": "form"
          },
          {
            "name": "repository_username",
            "location": "form"
          },
          {
            "name": "repository_token",
            "location": "form"
          }
        ]
      }
    },
    "owner": {
      "read": {
        "_type": "link",
        "url": "/api/datasets/{username}/{name}/owner/{member_username}/",
        "action": "get",
        "fields": [
          {
            "name": "name",
            "required": True,
            "location": "path"
          },
          {
            "name": "username",
            "required": True,
            "location": "path"
          },
          {
            "name": "member_username",
            "required": True,
            "location": "path"
          }
        ]
      }
    },
    "public_details": {
      "read": {
        "_type": "link",
        "url": "/api/datasets/public_details/{username}/{name}/",
        "action": "get",
        "description": "Return Public Dataset",
        "fields": [
          {
            "name": "name",
            "required": True,
            "location": "path"
          },
          {
            "name": "username",
            "required": True,
            "location": "path"
          }
        ]
      }
    },
    "readable": {
      "list": {
        "_type": "link",
        "url": "/api/datasets/readable/",
        "action": "get",
        "fields": [
          {
            "name": "page",
            "location": "query"
          },
          {
            "name": "limit",
            "location": "query"
          },
          {
            "name": "search",
            "location": "query"
          },
          {
            "name": "name",
            "location": "query"
          },
          {
            "name": "description",
            "location": "query"
          },
          {
            "name": "http_url_to_repo",
            "location": "query"
          },
          {
            "name": "created_at",
            "location": "query"
          },
          {
            "name": "owner",
            "location": "query"
          },
          {
            "name": "modified_at",
            "location": "query"
          }
        ]
      },
      "create": {
        "_type": "link",
        "url": "/api/datasets/readable/",
        "action": "post",
        "encoding": "application/json",
        "fields": [
          {
            "name": "bucket_name",
            "location": "form"
          },
          {
            "name": "icon",
            "location": "form"
          },
          {
            "name": "color",
            "location": "form"
          },
          {
            "name": "name",
            "required": True,
            "location": "form"
          },
          {
            "name": "source",
            "location": "form"
          },
          {
            "name": "full_name",
            "location": "form"
          },
          {
            "name": "parameters",
            "location": "form"
          },
          {
            "name": "description",
            "location": "form"
          },
          {
            "name": "http_url_to_repo",
            "location": "form"
          },
          {
            "name": "parent_repository",
            "location": "form"
          },
          {
            "name": "is_public",
            "location": "form"
          },
          {
            "name": "tags",
            "location": "form"
          },
          {
            "name": "repository_username",
            "location": "form"
          },
          {
            "name": "repository_token",
            "location": "form"
          }
        ]
      }
    },
    "share": {
      "create": {
        "_type": "link",
        "url": "/api/datasets/share/",
        "action": "post",
        "encoding": "application/json",
        "fields": [
          {
            "name": "list_users",
            "required": True,
            "location": "form"
          },
          {
            "name": "repository_id",
            "required": True,
            "location": "form"
          },
          {
            "name": "access_level",
            "location": "form"
          }
        ]
      }
    },
    "writable": {
      "list": {
        "_type": "link",
        "url": "/api/datasets/writable/",
        "action": "get",
        "fields": [
          {
            "name": "page",
            "location": "query"
          },
          {
            "name": "limit",
            "location": "query"
          },
          {
            "name": "search",
            "location": "query"
          },
          {
            "name": "name",
            "location": "query"
          },
          {
            "name": "description",
            "location": "query"
          },
          {
            "name": "http_url_to_repo",
            "location": "query"
          },
          {
            "name": "created_at",
            "location": "query"
          },
          {
            "name": "owner",
            "location": "query"
          },
          {
            "name": "modified_at",
            "location": "query"
          }
        ]
      },
      "create": {
        "_type": "link",
        "url": "/api/datasets/writable/",
        "action": "post",
        "encoding": "application/json",
        "fields": [
          {
            "name": "bucket_name",
            "location": "form"
          },
          {
            "name": "icon",
            "location": "form"
          },
          {
            "name": "color",
            "location": "form"
          },
          {
            "name": "name",
            "required": True,
            "location": "form"
          },
          {
            "name": "source",
            "location": "form"
          },
          {
            "name": "full_name",
            "location": "form"
          },
          {
            "name": "parameters",
            "location": "form"
          },
          {
            "name": "description",
            "location": "form"
          },
          {
            "name": "http_url_to_repo",
            "location": "form"
          },
          {
            "name": "parent_repository",
            "location": "form"
          },
          {
            "name": "is_public",
            "location": "form"
          },
          {
            "name": "tags",
            "location": "form"
          },
          {
            "name": "repository_username",
            "location": "form"
          },
          {
            "name": "repository_token",
            "location": "form"
          }
        ]
      }
    },
    "list": {
      "_type": "link",
      "url": "/api/datasets/",
      "action": "get",
      "description": "Dataset Create, List, Destroy Viewset",
      "fields": [
        {
          "name": "page",
          "location": "query"
        },
        {
          "name": "limit",
          "location": "query"
        },
        {
          "name": "search",
          "location": "query"
        },
        {
          "name": "name",
          "location": "query"
        },
        {
          "name": "description",
          "location": "query"
        },
        {
          "name": "http_url_to_repo",
          "location": "query"
        },
        {
          "name": "created_at",
          "location": "query"
        },
        {
          "name": "owner",
          "location": "query"
        },
        {
          "name": "modified_at",
          "location": "query"
        }
      ]
    },
    "create": {
      "_type": "link",
      "url": "/api/datasets/",
      "action": "post",
      "encoding": "application/json",
      "description": "Dataset Create, List, Destroy Viewset",
      "fields": [
        {
          "name": "bucket_name",
          "location": "form"
        },
        {
          "name": "icon",
          "location": "form"
        },
        {
          "name": "color",
          "location": "form"
        },
        {
          "name": "name",
          "required": True,
          "location": "form"
        },
        {
          "name": "source",
          "location": "form"
        },
        {
          "name": "full_name",
          "location": "form"
        },
        {
          "name": "parameters",
          "location": "form"
        },
        {
          "name": "description",
          "location": "form"
        },
        {
          "name": "http_url_to_repo",
          "location": "form"
        },
        {
          "name": "parent_repository",
          "location": "form"
        },
        {
          "name": "is_public",
          "location": "form"
        },
        {
          "name": "tags",
          "location": "form"
        },
        {
          "name": "repository_username",
          "location": "form"
        },
        {
          "name": "repository_token",
          "location": "form"
        }
      ]
    }
  },
  "docker_images": {
    "list": {
      "_type": "link",
      "url": "/api/docker_images/",
      "action": "get",
      "description": "Basic List View for Frameworks"
    }
  },
  "events": {
    "list": {
      "_type": "link",
      "url": "/api/events/",
      "action": "get",
      "fields": [
        {
          "name": "page",
          "location": "query"
        },
        {
          "name": "limit",
          "location": "query"
        },
        {
          "name": "search",
          "location": "query"
        },
        {
          "name": "job",
          "location": "query"
        },
        {
          "name": "job_run",
          "location": "query"
        },
        {
          "name": "event_type",
          "location": "query"
        },
        {
          "name": "repository",
          "location": "query"
        },
        {
          "name": "event_level",
          "location": "query"
        },
        {
          "name": "ordering",
          "location": "query"
        }
      ]
    },
    "create": {
      "_type": "link",
      "url": "/api/events/",
      "action": "post",
      "encoding": "application/json",
      "description": "We Add user as kwargs to use it later in preform create",
      "fields": [
        {
          "name": "repository",
          "location": "form"
        },
        {
          "name": "job",
          "location": "form"
        },
        {
          "name": "job_run",
          "location": "form"
        },
        {
          "name": "event_level",
          "location": "form"
        },
        {
          "name": "event_type",
          "location": "form"
        },
        {
          "name": "event_content",
          "location": "form"
        }
      ]
    },
    "read": {
      "_type": "link",
      "url": "/api/events/{event_id}/",
      "action": "get",
      "fields": [
        {
          "name": "event_id",
          "required": True,
          "location": "path"
        }
      ]
    },
    "update": {
      "_type": "link",
      "url": "/api/events/{event_id}/",
      "action": "put",
      "encoding": "application/json",
      "fields": [
        {
          "name": "event_id",
          "required": True,
          "location": "path"
        },
        {
          "name": "repository",
          "location": "form"
        },
        {
          "name": "job",
          "location": "form"
        },
        {
          "name": "job_run",
          "location": "form"
        },
        {
          "name": "event_level",
          "location": "form"
        },
        {
          "name": "event_type",
          "location": "form"
        },
        {
          "name": "event_content",
          "location": "form"
        }
      ]
    },
    "partial_update": {
      "_type": "link",
      "url": "/api/events/{event_id}/",
      "action": "patch",
      "encoding": "application/json",
      "fields": [
        {
          "name": "event_id",
          "required": True,
          "location": "path"
        },
        {
          "name": "repository",
          "location": "form"
        },
        {
          "name": "job",
          "location": "form"
        },
        {
          "name": "job_run",
          "location": "form"
        },
        {
          "name": "event_level",
          "location": "form"
        },
        {
          "name": "event_type",
          "location": "form"
        },
        {
          "name": "event_content",
          "location": "form"
        }
      ]
    },
    "delete": {
      "_type": "link",
      "url": "/api/events/{event_id}/",
      "action": "delete",
      "fields": [
        {
          "name": "event_id",
          "required": True,
          "location": "path"
        }
      ]
    }
  },
  "google": {
    "login": {
      "create": {
        "_type": "link",
        "url": "/api/google/login",
        "action": "post"
      }
    }
  },
  "instance-types": {
    "list": {
      "_type": "link",
      "url": "/api/instance-types/",
      "action": "get",
      "description": "Basic List View for Instance Type",
      "fields": [
        {
          "name": "search",
          "location": "query"
        },
        {
          "name": "show_for_ps",
          "location": "query"
        },
        {
          "name": "show_for_workers",
          "location": "query"
        },
        {
          "name": "type",
          "location": "query"
        }
      ]
    }
  },
  "invoices": {
    "list": {
      "_type": "link",
      "url": "/api/invoices/",
      "action": "get",
      "description": "Returns a List of Invoices for request User",
      "fields": [
        {
          "name": "page",
          "location": "query"
        },
        {
          "name": "limit",
          "location": "query"
        }
      ]
    },
    "read": {
      "_type": "link",
      "url": "/api/invoices/{invoice_id}/",
      "action": "get",
      "description": "Returns a invoice object from stripe for request User",
      "fields": [
        {
          "name": "invoice_id",
          "required": True,
          "location": "path"
        }
      ]
    }
  },
  "job_runs": {
    "list": {
      "_type": "link",
      "url": "/api/job_runs/",
      "action": "get",
      "description": "Basic List View for JobRun",
      "fields": [
        {
          "name": "page",
          "location": "query"
        },
        {
          "name": "limit",
          "location": "query"
        },
        {
          "name": "ordering",
          "location": "query"
        },
        {
          "name": "search",
          "location": "query"
        },
        {
          "name": "job",
          "location": "query"
        },
        {
          "name": "status",
          "location": "query"
        },
        {
          "name": "is_paid",
          "location": "query"
        },
        {
          "name": "is_successful",
          "location": "query"
        },
        {
          "name": "is_terminated",
          "location": "query"
        },
        {
          "name": "launched_at",
          "location": "query"
        }
      ]
    }
  },
  "jobs": {
    "active": {
      "list": {
        "_type": "link",
        "url": "/api/jobs/active/",
        "action": "get",
        "fields": [
          {
            "name": "page",
            "location": "query"
          },
          {
            "name": "limit",
            "location": "query"
          },
          {
            "name": "search",
            "location": "query"
          },
          {
            "name": "job_id",
            "location": "query"
          },
          {
            "name": "status",
            "location": "query"
          },
          {
            "name": "repository",
            "location": "query"
          },
          {
            "name": "datasets",
            "location": "query"
          },
          {
            "name": "display_name",
            "location": "query"
          },
          {
            "name": "created_at",
            "location": "query"
          },
          {
            "name": "created_by",
            "location": "query"
          },
          {
            "name": "type",
            "location": "query"
          }
        ]
      }
    },
    "file": {
      "read": {
        "_type": "link",
        "url": "/api/jobs/{job_id}/file/{filename}",
        "action": "get",
        "fields": [
          {
            "name": "job_id",
            "required": True,
            "location": "path"
          },
          {
            "name": "filename",
            "required": True,
            "location": "path"
          }
        ]
      }
    },
    "files": {
      "list": {
        "_type": "link",
        "url": "/api/jobs/{job_id}/files/",
        "action": "get",
        "fields": [
          {
            "name": "job_id",
            "required": True,
            "location": "path"
          }
        ]
      }
    },
    "members": {
      "confirm": {
        "list": {
          "_type": "link",
          "url": "/api/jobs/{job_id}/members/{username}/confirm/",
          "action": "get",
          "fields": [
            {
              "name": "job_id",
              "required": True,
              "location": "path"
            },
            {
              "name": "username",
              "required": True,
              "location": "path"
            }
          ]
        }
      },
      "expire": {
        "list": {
          "_type": "link",
          "url": "/api/jobs/{job_id}/members/{username}/expire/",
          "action": "get",
          "fields": [
            {
              "name": "job_id",
              "required": True,
              "location": "path"
            },
            {
              "name": "username",
              "required": True,
              "location": "path"
            }
          ]
        }
      }
    },
    "permissions": {
      "session": {
        "list": {
          "_type": "link",
          "url": "/api/jobs/{job_id}/permissions/session/",
          "action": "get",
          "fields": [
            {
              "name": "job_id",
              "required": True,
              "location": "path"
            }
          ]
        }
      },
      "user": {
        "read": {
          "_type": "link",
          "url": "/api/jobs/{job_id}/permissions/user/{username}/",
          "action": "get",
          "fields": [
            {
              "name": "job_id",
              "required": True,
              "location": "path"
            },
            {
              "name": "username",
              "required": True,
              "location": "path"
            }
          ]
        }
      }
    },
    "running": {
      "list": {
        "_type": "link",
        "url": "/api/jobs/running/",
        "action": "get",
        "fields": [
          {
            "name": "page",
            "location": "query"
          },
          {
            "name": "limit",
            "location": "query"
          },
          {
            "name": "search",
            "location": "query"
          },
          {
            "name": "job_id",
            "location": "query"
          },
          {
            "name": "status",
            "location": "query"
          },
          {
            "name": "repository",
            "location": "query"
          },
          {
            "name": "datasets",
            "location": "query"
          },
          {
            "name": "display_name",
            "location": "query"
          },
          {
            "name": "created_at",
            "location": "query"
          },
          {
            "name": "created_by",
            "location": "query"
          },
          {
            "name": "type",
            "location": "query"
          }
        ]
      }
    },
    "list": {
      "_type": "link",
      "url": "/api/jobs/",
      "action": "get",
      "fields": [
        {
          "name": "page",
          "location": "query"
        },
        {
          "name": "limit",
          "location": "query"
        },
        {
          "name": "search",
          "location": "query"
        },
        {
          "name": "job_id",
          "location": "query"
        },
        {
          "name": "status",
          "location": "query"
        },
        {
          "name": "repository",
          "location": "query"
        },
        {
          "name": "datasets",
          "location": "query"
        },
        {
          "name": "display_name",
          "location": "query"
        },
        {
          "name": "created_at",
          "location": "query"
        },
        {
          "name": "created_by",
          "location": "query"
        },
        {
          "name": "type",
          "location": "query"
        }
      ]
    },
    "create": {
      "_type": "link",
      "url": "/api/jobs/",
      "action": "post",
      "encoding": "application/json",
      "description": "We Add user as kwargs to use it later in preform create",
      "fields": [
        {
          "name": "repository",
          "required": True,
          "location": "form"
        },
        {
          "name": "display_name",
          "location": "form"
        },
        {
          "name": "description",
          "location": "form"
        },
        {
          "name": "launched_at",
          "location": "form"
        },
        {
          "name": "terminated_at",
          "location": "form"
        },
        {
          "name": "datasets_set",
          "location": "form"
        },
        {
          "name": "git_commit_hash",
          "location": "form"
        },
        {
          "name": "git_commit",
          "location": "form"
        },
        {
          "name": "git_branch",
          "location": "form"
        },
        {
          "name": "tags",
          "location": "form"
        },
        {
          "name": "user_panel",
          "location": "form"
        },
        {
          "name": "parameters",
          "required": True,
          "location": "form"
        },
        {
          "name": "resources",
          "location": "form"
        }
      ]
    },
    "start_generic": {
      "_type": "link",
      "url": "/api/jobs/start/",
      "action": "post",
      "encoding": "application/json",
      "fields": [
        {
          "name": "job_identifier",
          "required": True,
          "location": "form"
        }
      ]
    },
    "read": {
      "_type": "link",
      "url": "/api/jobs/{job_id}/",
      "action": "get",
      "fields": [
        {
          "name": "job_id",
          "required": True,
          "location": "path"
        }
      ]
    },
    "update": {
      "_type": "link",
      "url": "/api/jobs/{job_id}/",
      "action": "put",
      "encoding": "application/json",
      "fields": [
        {
          "name": "job_id",
          "required": True,
          "location": "path"
        },
        {
          "name": "repository",
          "required": True,
          "location": "form"
        },
        {
          "name": "display_name",
          "location": "form"
        },
        {
          "name": "description",
          "location": "form"
        },
        {
          "name": "launched_at",
          "location": "form"
        },
        {
          "name": "terminated_at",
          "location": "form"
        },
        {
          "name": "datasets_set",
          "location": "form"
        },
        {
          "name": "git_commit_hash",
          "location": "form"
        },
        {
          "name": "git_commit",
          "location": "form"
        },
        {
          "name": "git_branch",
          "location": "form"
        },
        {
          "name": "tags",
          "location": "form"
        },
        {
          "name": "user_panel",
          "location": "form"
        },
        {
          "name": "parameters",
          "required": True,
          "location": "form"
        },
        {
          "name": "resources",
          "location": "form"
        }
      ]
    },
    "partial_update": {
      "_type": "link",
      "url": "/api/jobs/{job_id}/",
      "action": "patch",
      "encoding": "application/json",
      "fields": [
        {
          "name": "job_id",
          "required": True,
          "location": "path"
        },
        {
          "name": "repository",
          "location": "form"
        },
        {
          "name": "display_name",
          "location": "form"
        },
        {
          "name": "description",
          "location": "form"
        },
        {
          "name": "launched_at",
          "location": "form"
        },
        {
          "name": "terminated_at",
          "location": "form"
        },
        {
          "name": "datasets_set",
          "location": "form"
        },
        {
          "name": "git_commit_hash",
          "location": "form"
        },
        {
          "name": "git_commit",
          "location": "form"
        },
        {
          "name": "git_branch",
          "location": "form"
        },
        {
          "name": "tags",
          "location": "form"
        },
        {
          "name": "user_panel",
          "location": "form"
        },
        {
          "name": "parameters",
          "location": "form"
        },
        {
          "name": "resources",
          "location": "form"
        }
      ]
    },
    "delete": {
      "_type": "link",
      "url": "/api/jobs/{job_id}/",
      "action": "delete",
      "fields": [
        {
          "name": "job_id",
          "required": True,
          "location": "path"
        }
      ]
    },
    "start": {
      "_type": "link",
      "url": "/api/jobs/{job_id}/start/",
      "action": "get",
      "fields": [
        {
          "name": "job_id",
          "required": True,
          "location": "path"
        }
      ]
    },
    "status": {
      "_type": "link",
      "url": "/api/jobs/{job_id}/status/",
      "action": "get",
      "description": "This view should return a job-monitor task results from job master based on given job_run",
      "fields": [
        {
          "name": "job_id",
          "required": True,
          "location": "path"
        }
      ]
    },
    "stop": {
      "_type": "link",
      "url": "/api/jobs/{job_id}/stop/",
      "action": "get",
      "fields": [
        {
          "name": "job_id",
          "required": True,
          "location": "path"
        }
      ]
    }
  },
  "list_users": {
    "list": {
      "_type": "link",
      "url": "/api/list_users/",
      "action": "get",
      "description": "Authenticated users can get a list of other users’ basic information.",
      "fields": [
        {
          "name": "page",
          "location": "query"
        },
        {
          "name": "limit",
          "location": "query"
        },
        {
          "name": "search",
          "location": "query"
        }
      ]
    }
  },
  "notebook_by_name": {
    "read": {
      "_type": "link",
      "url": "/api/notebook_by_name/{username}/{display_name}/",
      "action": "get",
      "fields": [
        {
          "name": "username",
          "required": True,
          "location": "path"
        },
        {
          "name": "display_name",
          "required": True,
          "location": "path"
        }
      ]
    }
  },
  "notebooks": {
    "snapshots": {
      "list": {
        "_type": "link",
        "url": "/api/notebooks/{job_id}/snapshots/",
        "action": "get",
        "fields": [
          {
            "name": "job_id",
            "required": True,
            "location": "path"
          },
          {
            "name": "page",
            "location": "query"
          },
          {
            "name": "limit",
            "location": "query"
          },
          {
            "name": "search",
            "location": "query"
          }
        ]
      },
      "create": {
        "_type": "link",
        "url": "/api/notebooks/{job_id}/snapshots/",
        "action": "post",
        "encoding": "application/json",
        "fields": [
          {
            "name": "job_id",
            "required": True,
            "location": "path"
          },
          {
            "name": "snapshot_name",
            "location": "form"
          }
        ]
      },
      "read": {
        "_type": "link",
        "url": "/api/notebooks/{job_id}/snapshots/{snapshot_name}/",
        "action": "get",
        "fields": [
          {
            "name": "job_id",
            "required": True,
            "location": "path"
          },
          {
            "name": "snapshot_name",
            "required": True,
            "location": "path"
          }
        ]
      },
      "delete": {
        "_type": "link",
        "url": "/api/notebooks/{job_id}/snapshots/{snapshot_name}/",
        "action": "delete",
        "fields": [
          {
            "name": "job_id",
            "required": True,
            "location": "path"
          },
          {
            "name": "snapshot_name",
            "required": True,
            "location": "path"
          }
        ]
      }
    },
    "list": {
      "_type": "link",
      "url": "/api/notebooks/",
      "action": "get",
      "fields": [
        {
          "name": "page",
          "location": "query"
        },
        {
          "name": "limit",
          "location": "query"
        },
        {
          "name": "search",
          "location": "query"
        },
        {
          "name": "job_id",
          "location": "query"
        },
        {
          "name": "status",
          "location": "query"
        },
        {
          "name": "repository",
          "location": "query"
        },
        {
          "name": "datasets",
          "location": "query"
        },
        {
          "name": "display_name",
          "location": "query"
        },
        {
          "name": "created_at",
          "location": "query"
        },
        {
          "name": "created_by",
          "location": "query"
        },
        {
          "name": "type",
          "location": "query"
        }
      ]
    },
    "create": {
      "_type": "link",
      "url": "/api/notebooks/",
      "action": "post",
      "encoding": "application/json",
      "description": "We Add user as kwargs to use it later in preform create",
      "fields": [
        {
          "name": "repository",
          "location": "form"
        },
        {
          "name": "display_name",
          "required": True,
          "location": "form"
        },
        {
          "name": "description",
          "location": "form"
        },
        {
          "name": "launched_at",
          "location": "form"
        },
        {
          "name": "terminated_at",
          "location": "form"
        },
        {
          "name": "datasets_set",
          "location": "form"
        },
        {
          "name": "git_commit_hash",
          "location": "form"
        },
        {
          "name": "git_commit",
          "location": "form"
        },
        {
          "name": "git_branch",
          "location": "form"
        },
        {
          "name": "logs",
          "location": "form"
        },
        {
          "name": "tags",
          "location": "form"
        },
        {
          "name": "user_panel",
          "location": "form"
        },
        {
          "name": "parameters",
          "required": True,
          "location": "form"
        },
        {
          "name": "resources",
          "location": "form"
        }
      ]
    },
    "read": {
      "_type": "link",
      "url": "/api/notebooks/{job_id}/",
      "action": "get",
      "fields": [
        {
          "name": "job_id",
          "required": True,
          "location": "path"
        }
      ]
    },
    "update": {
      "_type": "link",
      "url": "/api/notebooks/{job_id}/",
      "action": "put",
      "encoding": "application/json",
      "fields": [
        {
          "name": "job_id",
          "required": True,
          "location": "path"
        },
        {
          "name": "repository",
          "location": "form"
        },
        {
          "name": "display_name",
          "required": True,
          "location": "form"
        },
        {
          "name": "description",
          "location": "form"
        },
        {
          "name": "launched_at",
          "location": "form"
        },
        {
          "name": "terminated_at",
          "location": "form"
        },
        {
          "name": "datasets_set",
          "location": "form"
        },
        {
          "name": "git_commit_hash",
          "location": "form"
        },
        {
          "name": "git_commit",
          "location": "form"
        },
        {
          "name": "git_branch",
          "location": "form"
        },
        {
          "name": "logs",
          "location": "form"
        },
        {
          "name": "tags",
          "location": "form"
        },
        {
          "name": "user_panel",
          "location": "form"
        },
        {
          "name": "parameters",
          "required": True,
          "location": "form"
        },
        {
          "name": "resources",
          "location": "form"
        }
      ]
    },
    "partial_update": {
      "_type": "link",
      "url": "/api/notebooks/{job_id}/",
      "action": "patch",
      "encoding": "application/json",
      "fields": [
        {
          "name": "job_id",
          "required": True,
          "location": "path"
        },
        {
          "name": "repository",
          "location": "form"
        },
        {
          "name": "description",
          "location": "form"
        },
        {
          "name": "datasets_set",
          "location": "form"
        },
        {
          "name": "git_commit_hash",
          "location": "form"
        },
        {
          "name": "git_commit",
          "location": "form"
        },
        {
          "name": "git_branch",
          "location": "form"
        },
        {
          "name": "parameters",
          "location": "form"
        },
        {
          "name": "resources",
          "location": "form"
        }
      ]
    },
    "delete": {
      "_type": "link",
      "url": "/api/notebooks/{job_id}/",
      "action": "delete",
      "fields": [
        {
          "name": "job_id",
          "required": True,
          "location": "path"
        }
      ]
    },
    "start": {
      "_type": "link",
      "url": "/api/notebooks/{job_id}/start/",
      "action": "post",
      "encoding": "application/json",
      "fields": [
        {
          "name": "job_id",
          "required": True,
          "location": "path"
        },
        {
          "name": "snapshot_name",
          "location": "form"
        }
      ]
    },
    "stop": {
      "_type": "link",
      "url": "/api/notebooks/{job_id}/stop/",
      "action": "post",
      "encoding": "application/json",
      "fields": [
        {
          "name": "job_id",
          "required": True,
          "location": "path"
        },
        {
          "name": "snapshot_name",
          "location": "form"
        }
      ]
    }
  },
  "profile": {
    "list": {
      "_type": "link",
      "url": "/api/profile/",
      "action": "get",
      "description": "Basic User Profile API View",
      "fields": [
        {
          "name": "limit",
          "location": "query"
        },
        {
          "name": "offset",
          "location": "query"
        }
      ]
    },
    "update": {
      "_type": "link",
      "url": "/api/profile/",
      "action": "put",
      "encoding": "application/json",
      "description": "Basic User Profile API View",
      "fields": [
        {
          "name": "github_oauth_token",
          "location": "form"
        },
        {
          "name": "gitlab_oauth_token",
          "location": "form"
        },
        {
          "name": "github_username",
          "location": "form"
        },
        {
          "name": "gitlab_username",
          "location": "form"
        },
        {
          "name": "welcome_screen",
          "location": "form"
        },
        {
          "name": "first_name",
          "location": "form"
        },
        {
          "name": "last_name",
          "location": "form"
        },
        {
          "name": "website_url",
          "location": "form"
        },
        {
          "name": "monthly_cost_limit",
          "location": "form"
        },
        {
          "name": "promotional_code",
          "location": "form"
        },
        {
          "name": "credits",
          "location": "form"
        },
        {
          "name": "total_storage",
          "location": "form"
        },
        {
          "name": "biography",
          "location": "form"
        },
        {
          "name": "fields_of_interest",
          "location": "form"
        },
        {
          "name": "city",
          "location": "form"
        },
        {
          "name": "country",
          "location": "form"
        },
        {
          "name": "github",
          "location": "form"
        },
        {
          "name": "linkedin",
          "location": "form"
        },
        {
          "name": "twitter",
          "location": "form"
        },
        {
          "name": "organization",
          "location": "form"
        },
        {
          "name": "aws_iam",
          "location": "form"
        },
        {
          "name": "aws_iam_access_key",
          "location": "form"
        },
        {
          "name": "aws_iam_secret_key",
          "location": "form"
        },
        {
          "name": "gcp_client_id",
          "location": "form"
        },
        {
          "name": "gcp_project_id",
          "location": "form"
        },
        {
          "name": "gcp_client_secret",
          "location": "form"
        },
        {
          "name": "gcp_token",
          "location": "form"
        },
        {
          "name": "gcp_refresh_token",
          "location": "form"
        }
      ]
    }
  },
  "projects": {
    "details": {
      "read": {
        "_type": "link",
        "url": "/api/projects/details/{username}/{name}/",
        "action": "get",
        "description": "Updates, Removes an existing project.",
        "fields": [
          {
            "name": "name",
            "required": True,
            "location": "path"
          },
          {
            "name": "username",
            "required": True,
            "location": "path"
          }
        ]
      },
      "update": {
        "_type": "link",
        "url": "/api/projects/details/{username}/{name}/",
        "action": "put",
        "encoding": "application/json",
        "description": "Updates, Removes an existing project.",
        "fields": [
          {
            "name": "name",
            "required": True,
            "location": "path"
          },
          {
            "name": "username",
            "required": True,
            "location": "path"
          },
          {
            "name": "full_name",
            "location": "form"
          },
          {
            "name": "parameters",
            "location": "form"
          },
          {
            "name": "description",
            "location": "form"
          },
          {
            "name": "parent_repository",
            "location": "form"
          },
          {
            "name": "is_public",
            "location": "form"
          },
          {
            "name": "tags",
            "location": "form"
          },
          {
            "name": "source",
            "location": "form"
          },
          {
            "name": "repository_username",
            "location": "form"
          },
          {
            "name": "repository_token",
            "location": "form"
          }
        ]
      },
      "partial_update": {
        "_type": "link",
        "url": "/api/projects/details/{username}/{name}/",
        "action": "patch",
        "encoding": "application/json",
        "description": "Updates, Removes an existing project.",
        "fields": [
          {
            "name": "name",
            "required": True,
            "location": "path"
          },
          {
            "name": "username",
            "required": True,
            "location": "path"
          },
          {
            "name": "full_name",
            "location": "form"
          },
          {
            "name": "parameters",
            "location": "form"
          },
          {
            "name": "description",
            "location": "form"
          },
          {
            "name": "parent_repository",
            "location": "form"
          },
          {
            "name": "is_public",
            "location": "form"
          },
          {
            "name": "tags",
            "location": "form"
          },
          {
            "name": "source",
            "location": "form"
          },
          {
            "name": "repository_username",
            "location": "form"
          },
          {
            "name": "repository_token",
            "location": "form"
          }
        ]
      },
      "delete": {
        "_type": "link",
        "url": "/api/projects/details/{username}/{name}/",
        "action": "delete",
        "description": "Updates, Removes an existing project.",
        "fields": [
          {
            "name": "name",
            "required": True,
            "location": "path"
          },
          {
            "name": "username",
            "required": True,
            "location": "path"
          }
        ]
      }
    },
    "details_id": {
      "read": {
        "_type": "link",
        "url": "/api/projects/details_id/{id}/",
        "action": "get",
        "fields": [
          {
            "name": "id",
            "required": True,
            "location": "path"
          }
        ]
      },
      "update": {
        "_type": "link",
        "url": "/api/projects/details_id/{id}/",
        "action": "put",
        "encoding": "application/json",
        "fields": [
          {
            "name": "id",
            "required": True,
            "location": "path"
          },
          {
            "name": "full_name",
            "location": "form"
          },
          {
            "name": "parameters",
            "location": "form"
          },
          {
            "name": "description",
            "location": "form"
          },
          {
            "name": "parent_repository",
            "location": "form"
          },
          {
            "name": "is_public",
            "location": "form"
          },
          {
            "name": "tags",
            "location": "form"
          },
          {
            "name": "source",
            "location": "form"
          },
          {
            "name": "repository_username",
            "location": "form"
          },
          {
            "name": "repository_token",
            "location": "form"
          }
        ]
      },
      "partial_update": {
        "_type": "link",
        "url": "/api/projects/details_id/{id}/",
        "action": "patch",
        "encoding": "application/json",
        "fields": [
          {
            "name": "id",
            "required": True,
            "location": "path"
          },
          {
            "name": "full_name",
            "location": "form"
          },
          {
            "name": "parameters",
            "location": "form"
          },
          {
            "name": "description",
            "location": "form"
          },
          {
            "name": "parent_repository",
            "location": "form"
          },
          {
            "name": "is_public",
            "location": "form"
          },
          {
            "name": "tags",
            "location": "form"
          },
          {
            "name": "source",
            "location": "form"
          },
          {
            "name": "repository_username",
            "location": "form"
          },
          {
            "name": "repository_token",
            "location": "form"
          }
        ]
      },
      "delete": {
        "_type": "link",
        "url": "/api/projects/details_id/{id}/",
        "action": "delete",
        "fields": [
          {
            "name": "id",
            "required": True,
            "location": "path"
          }
        ]
      }
    },
    "file": {
      "read": {
        "_type": "link",
        "url": "/api/projects/{username}/{name}/file/{sha}/",
        "action": "get",
        "description": "This view return decoded file content from gitlab_api\n:param request:\n:param name:\n:return:",
        "fields": [
          {
            "name": "name",
            "required": True,
            "location": "path"
          },
          {
            "name": "sha",
            "required": True,
            "location": "path"
          },
          {
            "name": "username",
            "required": True,
            "location": "path"
          }
        ]
      }
    },
    "files": {
      "list": {
        "_type": "link",
        "url": "/api/projects/{username}/{name}/files/",
        "action": "get",
        "description": "This view return file list tree for given path\n:param request:\n:param name:\n:return:",
        "fields": [
          {
            "name": "name",
            "required": True,
            "location": "path"
          },
          {
            "name": "username",
            "required": True,
            "location": "path"
          }
        ]
      },
      "read": {
        "_type": "link",
        "url": "/api/projects/{username}/{name}/files/{path}/",
        "action": "get",
        "description": "This view return file list tree for given path\n:param request:\n:param name:\n:return:",
        "fields": [
          {
            "name": "name",
            "required": True,
            "location": "path"
          },
          {
            "name": "username",
            "required": True,
            "location": "path"
          },
          {
            "name": "path",
            "required": True,
            "location": "path"
          }
        ]
      }
    },
    "link": {
      "create": {
        "_type": "link",
        "url": "/api/projects/link/",
        "action": "post",
        "encoding": "application/json",
        "fields": [
          {
            "name": "name",
            "required": True,
            "location": "form"
          },
          {
            "name": "full_name",
            "location": "form"
          },
          {
            "name": "parameters",
            "location": "form"
          },
          {
            "name": "description",
            "location": "form"
          },
          {
            "name": "http_url_to_repo",
            "location": "form"
          },
          {
            "name": "is_public",
            "location": "form"
          },
          {
            "name": "tags",
            "location": "form"
          },
          {
            "name": "source",
            "location": "form"
          },
          {
            "name": "repository_username",
            "location": "form"
          },
          {
            "name": "repository_token",
            "location": "form"
          }
        ]
      }
    },
    "members": {
      "expire": {
        "list": {
          "_type": "link",
          "url": "/api/projects/{username}/{name}/members/{member_username}/expire/",
          "action": "get",
          "fields": [
            {
              "name": "name",
              "required": True,
              "location": "path"
            },
            {
              "name": "username",
              "required": True,
              "location": "path"
            },
            {
              "name": "member_username",
              "required": True,
              "location": "path"
            }
          ]
        }
      },
      "list": {
        "_type": "link",
        "url": "/api/projects/{username}/{name}/members/",
        "action": "get",
        "description": "ListAPIView returns :model:'projects.RepositoryMembership' model based on project",
        "fields": [
          {
            "name": "name",
            "required": True,
            "location": "path"
          },
          {
            "name": "username",
            "required": True,
            "location": "path"
          },
          {
            "name": "limit",
            "location": "query"
          },
          {
            "name": "offset",
            "location": "query"
          }
        ]
      }
    },
    "new": {
      "create": {
        "_type": "link",
        "url": "/api/projects/new/",
        "action": "post",
        "encoding": "application/json",
        "fields": [
          {
            "name": "name",
            "required": True,
            "location": "form"
          },
          {
            "name": "full_name",
            "location": "form"
          },
          {
            "name": "description",
            "location": "form"
          },
          {
            "name": "http_url_to_repo",
            "location": "form"
          },
          {
            "name": "parent_repository",
            "location": "form"
          },
          {
            "name": "tags",
            "location": "form"
          },
          {
            "name": "source",
            "location": "form"
          },
          {
            "name": "repository_username",
            "location": "form"
          },
          {
            "name": "repository_token",
            "location": "form"
          }
        ]
      }
    },
    "owned": {
      "list": {
        "_type": "link",
        "url": "/api/projects/owned/",
        "action": "get",
        "description": "Get a list of projects which are owned by the authenticated user.",
        "fields": [
          {
            "name": "page",
            "location": "query"
          },
          {
            "name": "limit",
            "location": "query"
          }
        ]
      }
    },
    "owner": {
      "read": {
        "_type": "link",
        "url": "/api/projects/{username}/{name}/owner/{member_username}/",
        "action": "get",
        "fields": [
          {
            "name": "name",
            "required": True,
            "location": "path"
          },
          {
            "name": "username",
            "required": True,
            "location": "path"
          },
          {
            "name": "member_username",
            "required": True,
            "location": "path"
          }
        ]
      }
    },
    "public_details": {
      "read": {
        "_type": "link",
        "url": "/api/projects/public_details/{username}/{name}/",
        "action": "get",
        "description": "Return Public Project",
        "fields": [
          {
            "name": "name",
            "required": True,
            "location": "path"
          },
          {
            "name": "username",
            "required": True,
            "location": "path"
          }
        ]
      }
    },
    "readable": {
      "list": {
        "_type": "link",
        "url": "/api/projects/readable/",
        "action": "get",
        "fields": [
          {
            "name": "page",
            "location": "query"
          },
          {
            "name": "limit",
            "location": "query"
          }
        ]
      }
    },
    "share": {
      "create": {
        "_type": "link",
        "url": "/api/projects/share/",
        "action": "post",
        "encoding": "application/json",
        "fields": [
          {
            "name": "list_users",
            "required": True,
            "location": "form"
          },
          {
            "name": "repository_id",
            "required": True,
            "location": "form"
          },
          {
            "name": "access_level",
            "location": "form"
          }
        ]
      }
    },
    "writable": {
      "list": {
        "_type": "link",
        "url": "/api/projects/writable/",
        "action": "get",
        "fields": [
          {
            "name": "page",
            "location": "query"
          },
          {
            "name": "limit",
            "location": "query"
          }
        ]
      }
    },
    "list": {
      "_type": "link",
      "url": "/api/projects/",
      "action": "get",
      "description": "Project Create, List, Destroy Viewset",
      "fields": [
        {
          "name": "page",
          "location": "query"
        },
        {
          "name": "limit",
          "location": "query"
        },
        {
          "name": "search",
          "location": "query"
        },
        {
          "name": "name",
          "location": "query"
        },
        {
          "name": "description",
          "location": "query"
        },
        {
          "name": "http_url_to_repo",
          "location": "query"
        },
        {
          "name": "created_at",
          "location": "query"
        },
        {
          "name": "owner",
          "location": "query"
        },
        {
          "name": "modified_at",
          "location": "query"
        }
      ]
    },
    "create": {
      "_type": "link",
      "url": "/api/projects/",
      "action": "post",
      "encoding": "application/json",
      "description": "Project Create, List, Destroy Viewset",
      "fields": [
        {
          "name": "name",
          "required": True,
          "location": "form"
        },
        {
          "name": "full_name",
          "location": "form"
        },
        {
          "name": "parameters",
          "location": "form"
        },
        {
          "name": "description",
          "location": "form"
        },
        {
          "name": "http_url_to_repo",
          "location": "form"
        },
        {
          "name": "is_public",
          "location": "form"
        },
        {
          "name": "tags",
          "location": "form"
        },
        {
          "name": "source",
          "location": "form"
        },
        {
          "name": "repository_username",
          "location": "form"
        },
        {
          "name": "repository_token",
          "location": "form"
        }
      ]
    }
  },
  "register": {
    "create": {
      "_type": "link",
      "url": "/api/register/",
      "action": "post",
      "encoding": "application/json",
      "fields": [
        {
          "name": "username",
          "required": True,
          "location": "form"
        },
        {
          "name": "password",
          "required": True,
          "location": "form"
        },
        {
          "name": "email",
          "required": True,
          "location": "form"
        }
      ]
    }
  },
  "schema": {
    "list": {
      "_type": "link",
      "url": "/api/schema/",
      "action": "get"
    }
  },
  "send_invites": {
    "list": {
      "_type": "link",
      "url": "/api/send_invites/",
      "action": "get",
      "description": "This view handles project/dataset sharing and sending invites to new users\n:param request:\n:return:"
    },
    "create": {
      "_type": "link",
      "url": "/api/send_invites/",
      "action": "post",
      "description": "This view handles project/dataset sharing and sending invites to new users\n:param request:\n:return:"
    }
  },
  "share_job": {
    "create": {
      "_type": "link",
      "url": "/api/share_job/",
      "action": "post"
    }
  },
  "share_repository": {
    "create": {
      "_type": "link",
      "url": "/api/share_repository/",
      "action": "post",
      "encoding": "application/json",
      "fields": [
        {
          "name": "list_users",
          "required": True,
          "location": "form"
        },
        {
          "name": "repository_id",
          "required": True,
          "location": "form"
        },
        {
          "name": "access_level",
          "location": "form"
        }
      ]
    }
  },
  "subscribe": {
    "create": {
      "_type": "link",
      "url": "/api/subscribe/",
      "action": "post"
    }
  },
  "token": {
    "create": {
      "_type": "link",
      "url": "/api/token/",
      "action": "post",
      "encoding": "application/json",
      "description": "API View that receives a POST with a user's username and password.\n\nReturns a JSON Web Token that can be used for authenticated requests.",
      "fields": [
        {
          "name": "username",
          "required": True,
          "location": "form"
        },
        {
          "name": "password",
          "required": True,
          "location": "form"
        }
      ]
    }
  },
  "users": {
    "list": {
      "_type": "link",
      "url": "/api/users/",
      "action": "get",
      "description": "User creation\nCreates a new user. Note only administrators can create new users.\nUser will be created as inactive and the email confirmation flow will initiate to activate the user.",
      "fields": [
        {
          "name": "page",
          "location": "query"
        },
        {
          "name": "limit",
          "location": "query"
        }
      ]
    },
    "create": {
      "_type": "link",
      "url": "/api/users/",
      "action": "post",
      "encoding": "application/json",
      "description": "User creation\nCreates a new user. Note only administrators can create new users.\nUser will be created as inactive and the email confirmation flow will initiate to activate the user.",
      "fields": [
        {
          "name": "github_oauth_token",
          "location": "form"
        },
        {
          "name": "gitlab_oauth_token",
          "location": "form"
        },
        {
          "name": "github_username",
          "location": "form"
        },
        {
          "name": "gitlab_username",
          "location": "form"
        },
        {
          "name": "welcome_screen",
          "location": "form"
        },
        {
          "name": "first_name",
          "location": "form"
        },
        {
          "name": "last_name",
          "location": "form"
        },
        {
          "name": "website_url",
          "location": "form"
        },
        {
          "name": "monthly_cost_limit",
          "location": "form"
        },
        {
          "name": "promotional_code",
          "location": "form"
        },
        {
          "name": "credits",
          "location": "form"
        },
        {
          "name": "total_storage",
          "location": "form"
        },
        {
          "name": "biography",
          "location": "form"
        },
        {
          "name": "fields_of_interest",
          "location": "form"
        },
        {
          "name": "city",
          "location": "form"
        },
        {
          "name": "country",
          "location": "form"
        },
        {
          "name": "github",
          "location": "form"
        },
        {
          "name": "linkedin",
          "location": "form"
        },
        {
          "name": "twitter",
          "location": "form"
        },
        {
          "name": "organization",
          "location": "form"
        },
        {
          "name": "aws_iam",
          "location": "form"
        },
        {
          "name": "aws_iam_access_key",
          "location": "form"
        },
        {
          "name": "aws_iam_secret_key",
          "location": "form"
        },
        {
          "name": "gcp_client_id",
          "location": "form"
        },
        {
          "name": "gcp_project_id",
          "location": "form"
        },
        {
          "name": "gcp_client_secret",
          "location": "form"
        },
        {
          "name": "gcp_token",
          "location": "form"
        },
        {
          "name": "gcp_refresh_token",
          "location": "form"
        }
      ]
    },
    "read": {
      "_type": "link",
      "url": "/api/users/{username}/",
      "action": "get",
      "description": "Modifies an existing user. Only administrators can change attributes of a user.",
      "fields": [
        {
          "name": "username",
          "required": True,
          "location": "path"
        }
      ]
    },
    "update": {
      "_type": "link",
      "url": "/api/users/{username}/",
      "action": "put",
      "encoding": "application/json",
      "description": "Modifies an existing user. Only administrators can change attributes of a user.",
      "fields": [
        {
          "name": "username",
          "required": True,
          "location": "path"
        },
        {
          "name": "github_oauth_token",
          "location": "form"
        },
        {
          "name": "gitlab_oauth_token",
          "location": "form"
        },
        {
          "name": "github_username",
          "location": "form"
        },
        {
          "name": "gitlab_username",
          "location": "form"
        },
        {
          "name": "welcome_screen",
          "location": "form"
        },
        {
          "name": "first_name",
          "location": "form"
        },
        {
          "name": "last_name",
          "location": "form"
        },
        {
          "name": "website_url",
          "location": "form"
        },
        {
          "name": "monthly_cost_limit",
          "location": "form"
        },
        {
          "name": "promotional_code",
          "location": "form"
        },
        {
          "name": "credits",
          "location": "form"
        },
        {
          "name": "total_storage",
          "location": "form"
        },
        {
          "name": "biography",
          "location": "form"
        },
        {
          "name": "fields_of_interest",
          "location": "form"
        },
        {
          "name": "city",
          "location": "form"
        },
        {
          "name": "country",
          "location": "form"
        },
        {
          "name": "github",
          "location": "form"
        },
        {
          "name": "linkedin",
          "location": "form"
        },
        {
          "name": "twitter",
          "location": "form"
        },
        {
          "name": "organization",
          "location": "form"
        },
        {
          "name": "aws_iam",
          "location": "form"
        },
        {
          "name": "aws_iam_access_key",
          "location": "form"
        },
        {
          "name": "aws_iam_secret_key",
          "location": "form"
        },
        {
          "name": "gcp_client_id",
          "location": "form"
        },
        {
          "name": "gcp_project_id",
          "location": "form"
        },
        {
          "name": "gcp_client_secret",
          "location": "form"
        },
        {
          "name": "gcp_token",
          "location": "form"
        },
        {
          "name": "gcp_refresh_token",
          "location": "form"
        }
      ]
    },
    "partial_update": {
      "_type": "link",
      "url": "/api/users/{username}/",
      "action": "patch",
      "encoding": "application/json",
      "description": "Modifies an existing user. Only administrators can change attributes of a user.",
      "fields": [
        {
          "name": "username",
          "required": True,
          "location": "path"
        },
        {
          "name": "github_oauth_token",
          "location": "form"
        },
        {
          "name": "gitlab_oauth_token",
          "location": "form"
        },
        {
          "name": "github_username",
          "location": "form"
        },
        {
          "name": "gitlab_username",
          "location": "form"
        },
        {
          "name": "welcome_screen",
          "location": "form"
        },
        {
          "name": "first_name",
          "location": "form"
        },
        {
          "name": "last_name",
          "location": "form"
        },
        {
          "name": "website_url",
          "location": "form"
        },
        {
          "name": "monthly_cost_limit",
          "location": "form"
        },
        {
          "name": "promotional_code",
          "location": "form"
        },
        {
          "name": "credits",
          "location": "form"
        },
        {
          "name": "total_storage",
          "location": "form"
        },
        {
          "name": "biography",
          "location": "form"
        },
        {
          "name": "fields_of_interest",
          "location": "form"
        },
        {
          "name": "city",
          "location": "form"
        },
        {
          "name": "country",
          "location": "form"
        },
        {
          "name": "github",
          "location": "form"
        },
        {
          "name": "linkedin",
          "location": "form"
        },
        {
          "name": "twitter",
          "location": "form"
        },
        {
          "name": "organization",
          "location": "form"
        },
        {
          "name": "aws_iam",
          "location": "form"
        },
        {
          "name": "aws_iam_access_key",
          "location": "form"
        },
        {
          "name": "aws_iam_secret_key",
          "location": "form"
        },
        {
          "name": "gcp_client_id",
          "location": "form"
        },
        {
          "name": "gcp_project_id",
          "location": "form"
        },
        {
          "name": "gcp_client_secret",
          "location": "form"
        },
        {
          "name": "gcp_token",
          "location": "form"
        },
        {
          "name": "gcp_refresh_token",
          "location": "form"
        }
      ]
    },
    "delete": {
      "_type": "link",
      "url": "/api/users/{username}/",
      "action": "delete",
      "description": "Modifies an existing user. Only administrators can change attributes of a user.",
      "fields": [
        {
          "name": "username",
          "required": True,
          "location": "path"
        }
      ]
    }
  },
  "waitlist": {
    "create": {
      "_type": "link",
      "url": "/api/waitlist/",
      "action": "post",
      "encoding": "application/json",
      "fields": [
        {
          "name": "email",
          "required": True,
          "location": "form"
        }
      ]
    }
  }
}
