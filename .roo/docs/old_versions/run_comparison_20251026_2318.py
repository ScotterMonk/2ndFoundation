import json
from schema_comparison import compare_schemas

# Model schema from SQLAlchemy models
model_schema = {
  "interaction_models.py": {
    "UserFavorite": {
      "table_name": "users_favorites",
      "columns": {
        "id": "Integer",
        "user_id": "Integer",
        "media_id": "Integer",
        "created_at": "DateTime"
      },
      "relationships": {
        "user": "User",
        "media": "Media"
      }
    },
    "UserRating": {
      "table_name": "users_ratings",
      "columns": {
        "id": "Integer",
        "user_id": "Integer",
        "media_id": "Integer",
        "rating": "Integer",
        "created_at": "DateTime"
      },
      "relationships": {
        "user": "User",
        "media": "Media"
      }
    },
    "UserMediaHistory": {
      "table_name": "users_media_history",
      "columns": {
        "id": "Integer",
        "user_id": "Integer",
        "media_id": "Integer",
        "playback_position_seconds": "Integer",
        "last_watched_at": "DateTime",
        "completed": "Boolean",
        "created_at": "DateTime"
      },
      "relationships": {
        "user": "User",
        "media": "Media"
      }
    },
    "UserMediaAffinity": {
      "table_name": "user_media_affinity",
      "columns": {
        "id": "Integer",
        "user_id": "Integer",
        "genre_id": "Integer",
        "affinity_score": "Float",
        "updated_at": "DateTime"
      },
      "relationships": {
        "user": "User",
        "genre": "Genre"
      }
    },
    "Playlist": {
      "table_name": "playlists",
      "columns": {
        "id": "Integer",
        "user_id": "Integer",
        "playlist_name": "String(255)",
        "is_public": "Boolean",
        "created_at": "DateTime",
        "updated_at": "DateTime"
      },
      "relationships": {
        "user": "User",
        "media_items": "PlaylistMediaItem"
      }
    },
    "PlaylistMediaItem": {
      "table_name": "playlists_media_items",
      "columns": {
        "id": "Integer",
        "playlist_id": "Integer",
        "media_id": "Integer",
        "sort_order": "Integer",
        "added_at": "DateTime"
      },
      "relationships": {
        "playlist": "Playlist",
        "media": "Media"
      }
    }
  },
  "media_models.py": {
    "MediaType": {
      "table_name": "media_types",
      "columns": {
        "id": "Integer",
        "type_name": "String(50)",
        "created_at": "DateTime"
      },
      "relationships": {
        "media_items": "Media"
      }
    },
    "Language": {
      "table_name": "languages",
      "columns": {
        "id": "Integer",
        "language_code": "String(10)",
        "language_name": "String(100)"
      },
      "relationships": {
        "media_items": "Media",
        "subtitles": "MediaSubtitle"
      }
    },
    "Genre": {
      "table_name": "genres",
      "columns": {
        "id": "Integer",
        "genre_name": "String(100)",
        "created_at": "DateTime"
      },
      "relationships": {
        "media_genres": "MediaGenre"
      }
    },
    "MediaCategory": {
      "table_name": "media_categories",
      "columns": {
        "id": "Integer",
        "category_name": "String(100)",
        "parent_category_id": "Integer",
        "created_at": "DateTime"
      },
      "relationships": {
        "parent_category": "MediaCategory",
        "sub_categories": "MediaCategory",
        "assignments": "MediaCategoryAssignment"
      }
    },
    "Media": {
      "table_name": "media",
      "columns": {
        "id": "Integer",
        "users_id": "Integer",
        "title": "String(255)",
        "description": "Text",
        "media_type_id": "Integer",
        "file_path": "String(512)",
        "thumbnail_path": "String(512)",
        "duration_seconds": "Integer",
        "tmdb_id": "Integer",
        "language_id": "Integer",
        "is_public": "Boolean",
        "is_processed": "Boolean",
        "processing_status": "String(20)",
        "created_at": "DateTime",
        "updated_at": "DateTime"
      },
      "relationships": {
        "media_type": "MediaType",
        "language": "Language",
        "episodes": "Episode",
        "files": "File",
        "subtitles": "MediaSubtitle",
        "categories": "MediaCategoryAssignment",
        "genres": "MediaGenre",
        "content_reports": "ContentReport"
      }
    },
    "Episode": {
      "table_name": "episodes",
      "columns": {
        "id": "Integer",
        "media_id": "Integer",
        "season_number": "Integer",
        "episode_number": "Integer",
        "title": "String(255)",
        "description": "Text",
        "file_path": "String(512)",
        "duration_seconds": "Integer",
        "created_at": "DateTime"
      },
      "relationships": {
        "media": "Media"
      }
    },
    "MediaQualityLevel": {
      "table_name": "media_quality_levels",
      "columns": {
        "id": "Integer",
        "quality_name": "String(50)",
        "resolution": "String(20)",
        "bitrate": "Integer",
        "created_at": "DateTime"
      },
      "relationships": {
        "files": "File"
      }
    },
    "MediaGenre": {
      "table_name": "media_genres",
      "columns": {
        "id": "Integer",
        "media_id": "Integer",
        "genre_id": "Integer"
      },
      "relationships": {
        "media": "Media",
        "genre": "Genre"
      }
    },
    "MediaSubtitle": {
      "table_name": "media_subtitles",
      "columns": {
        "id": "Integer",
        "media_id": "Integer",
        "language_id": "Integer",
        "subtitle_file_path": "String(512)",
        "created_at": "DateTime"
      },
      "relationships": {
        "media": "Media",
        "language": "Language"
      }
    },
    "MediaCategoryAssignment": {
      "table_name": "media_categories_assignments",
      "columns": {
        "id": "Integer",
        "media_id": "Integer",
        "category_id": "Integer",
        "created_at": "DateTime"
      },
      "relationships": {
        "media": "Media",
        "category": "MediaCategory"
      }
    },
    "ContentReport": {
      "table_name": "content_reports",
      "columns": {
        "id": "Integer",
        "media_id": "Integer",
        "user_id": "Integer",
        "report_reason": "String(255)",
        "details": "Text",
        "status": "String(50)",
        "created_at": "DateTime"
      },
      "relationships": {
        "media": "Media",
        "user": "User"
      }
    },
    "File": {
      "table_name": "files",
      "columns": {
        "id": "Integer",
        "media_id": "Integer",
        "quality_level_id": "Integer",
        "file_path": "String(512)",
        "file_size_bytes": "BigInteger",
        "created_at": "DateTime"
      },
      "relationships": {
        "media": "Media",
        "quality_level": "MediaQualityLevel"
      }
    },
    "MediaPerformer": {
      "table_name": "media_performers",
      "columns": {
        "id": "Integer",
        "name": "String(255)",
        "role": "String(100)",
        "bio": "Text",
        "created_at": "DateTime"
      },
      "relationships": {}
    }
  },
  "payment_models.py": {
    "TransactionType": {
      "table_name": "transactions_types",
      "columns": {
        "id": "Integer",
        "type_name": "String(100)",
        "description": "String(255)"
      },
      "relationships": {
        "transactions": "Transaction"
      }
    },
    "PaymentMethod": {
      "table_name": "payment_methods",
      "columns": {
        "id": "Integer",
        "method_name": "String(100)",
        "is_active": "Boolean",
        "created_at": "DateTime"
      },
      "relationships": {
        "payments": "Payment"
      }
    },
    "CreditPackage": {
      "table_name": "credit_packages",
      "columns": {
        "id": "Integer",
        "package_name": "String(100)",
        "credit_amount": "Integer",
        "price": "Numeric(10, 2)",
        "is_active": "Boolean",
        "created_at": "DateTime"
      },
      "relationships": {}
    },
    "SubscriptionPlan": {
      "table_name": "subscriptions_plans",
      "columns": {
        "id": "Integer",
        "plan_name": "String(100)",
        "price": "Numeric(10, 2)",
        "duration_days": "Integer",
        "features_json": "JSON",
        "is_active": "Boolean",
        "created_at": "DateTime"
      },
      "relationships": {
        "subscriptions": "Subscription"
      }
    },
    "Subscription": {
      "table_name": "subscriptions",
      "columns": {
        "id": "Integer",
        "user_id": "Integer",
        "plan_id": "Integer",
        "start_date": "DateTime",
        "end_date": "DateTime",
        "status": "String(20)",
        "auto_renew": "Boolean",
        "created_at": "DateTime"
      },
      "relationships": {
        "user": "User",
        "plan": "SubscriptionPlan",
        "history": "SubscriptionHistory"
      }
    },
    "Payment": {
      "table_name": "payments",
      "columns": {
        "id": "Integer",
        "users_id": "Integer",
        "payment_method_id": "Integer",
        "amount": "Numeric(10, 2)",
        "external_transaction_id": "String(255)",
        "payment_status": "String(50)",
        "created_at": "DateTime"
      },
      "relationships": {
        "user": "User",
        "payment_method": "PaymentMethod"
      }
    },
    "Transaction": {
      "table_name": "transactions",
      "columns": {
        "id": "Integer",
        "user_id": "Integer",
        "transaction_type_id": "Integer",
        "amount": "Numeric(10, 2)",
        "description": "String(255)",
        "created_at": "DateTime"
      },
      "relationships": {
        "user": "User",
        "transaction_type": "TransactionType"
      }
    },
    "CreditTransaction": {
      "table_name": "credit_transactions",
      "columns": {
        "id": "Integer",
        "user_id": "Integer",
        "credit_change": "Integer",
        "transaction_type": "String(100)",
        "reference_id": "Integer",
        "created_at": "DateTime"
      },
      "relationships": {
        "user": "User"
      }
    },
    "SubscriptionHistory": {
      "table_name": "subscriptions_history",
      "columns": {
        "id": "Integer",
        "subscription_id": "Integer",
        "action": "String(50)",
        "details_json": "JSON",
        "created_at": "DateTime"
      },
      "relationships": {
        "subscription": "Subscription"
      }
    }
  },
  "referral_models.py": {
    "ReferralCode": {
      "table_name": "referral_codes",
      "columns": {
        "id": "Integer",
        "user_id": "Integer",
        "code": "String(20)",
        "max_uses": "Integer",
        "current_uses": "Integer",
        "expires_at": "DateTime",
        "created_at": "DateTime"
      },
      "relationships": {
        "user": "User"
      }
    },
    "UserReferralEarning": {
      "table_name": "users_referral_earnings",
      "columns": {
        "id": "Integer",
        "referrer_id": "Integer",
        "referred_id": "Integer",
        "earning_amount": "Numeric(10, 2)",
        "created_at": "DateTime"
      },
      "relationships": {
        "referrer": "User",
        "referred": "User"
      }
    },
    "Invitation": {
      "table_name": "invitations",
      "columns": {
        "id": "Integer",
        "inviter_id": "Integer",
        "email": "String(120)",
        "invitation_code": "String(64)",
        "status": "String(20)",
        "created_at": "DateTime",
        "accepted_at": "DateTime"
      },
      "relationships": {
        "inviter": "User"
      }
    }
  },
  "reseller_models.py": {
    "ResellerDetail": {
      "table_name": "resellers_details",
      "columns": {
        "id": "Integer",
        "user_id": "Integer",
        "company_name": "String(255)",
        "contact_info_json": "JSON",
        "commission_rate": "Numeric(5, 4)",
        "created_at": "DateTime"
      },
      "relationships": {
        "user": "User"
      }
    },
    "ResellerSetting": {
      "table_name": "resellers_settings",
      "columns": {
        "id": "Integer",
        "user_id": "Integer",
        "settings_json": "JSON",
        "updated_at": "DateTime"
      },
      "relationships": {
        "user": "User"
      }
    },
    "ResellerAsset": {
      "table_name": "resellers_assets",
      "columns": {
        "id": "Integer",
        "user_id": "Integer",
        "asset_type": "String(50)",
        "file_path": "String(512)",
        "original_filename": "String(255)",
        "file_size": "Integer",
        "mime_type": "String(100)",
        "created_at": "DateTime"
      },
      "relationships": {
        "user": "User"
      }
    },
    "ResellerCommission": {
      "table_name": "resellers_commissions",
      "columns": {
        "id": "Integer",
        "reseller_id": "Integer",
        "transaction_id": "Integer",
        "commission_amount": "Numeric(10, 2)",
        "transaction_amount": "Numeric(10, 2)",
        "commission_rate_used": "Numeric(5, 4)",
        "created_at": "DateTime"
      },
      "relationships": {
        "reseller": "User"
      }
    }
  },
  "support_models.py": {
    "SupportTicket": {
      "table_name": "support_tickets",
      "columns": {
        "id": "Integer",
        "users_id": "Integer",
        "subject": "String(255)",
        "status": "String(50)",
        "priority": "String(20)",
        "created_at": "DateTime",
        "updated_at": "DateTime"
      },
      "relationships": {
        "user": "User",
        "messages": "TicketMessage"
      }
    },
    "TicketMessage": {
      "table_name": "tickets_messages",
      "columns": {
        "id": "Integer",
        "ticket_id": "Integer",
        "user_id": "Integer",
        "message": "Text",
        "is_staff_response": "Boolean",
        "created_at": "DateTime"
      },
      "relationships": {
        "ticket": "SupportTicket",
        "user": "User"
      }
    },
    "EventType": {
      "table_name": "events_types",
      "columns": {
        "id": "Integer",
        "event_name": "String(100)",
        "description": "String(255)"
      },
      "relationships": {
        "events": "Event"
      }
    },
    "Event": {
      "table_name": "events",
      "columns": {
        "id": "Integer",
        "user_id": "Integer",
        "event_type_id": "Integer",
        "details_json": "JSON",
        "created_at": "DateTime"
      },
      "relationships": {
        "user": "User",
        "event_type": "EventType"
      }
    },
    "SystemSetting": {
      "table_name": "system_settings",
      "columns": {
        "id": "Integer",
        "setting_key": "String(100)",
        "setting_value": "Text",
        "updated_at": "DateTime"
      },
      "relationships": {}
    },
    "APIKey": {
      "table_name": "api_keys",
      "columns": {
        "id": "Integer",
        "user_id": "Integer",
        "key_name": "String(100)",
        "api_key_hash": "String(128)",
        "permissions_json": "JSON",
        "is_active": "Boolean",
        "created_at": "DateTime",
        "last_used_at": "DateTime"
      },
      "relationships": {
        "user": "User"
      }
    }
  },
  "user_models.py": {
    "UserType": {
      "table_name": "users_types",
      "columns": {
        "id": "Integer",
        "code": "String(50)",
        "name": "String(50)",
        "description": "Text",
        "max_uploads": "Integer",
        "max_storage_mb": "Integer",
        "can_resell": "Boolean",
        "created_at": "DateTime",
        "updated_at": "DateTime",
        "created_by": "Integer",
        "updated_by": "Integer"
      },
      "relationships": {
        "users": "User"
      }
    },
    "User": {
      "table_name": "users",
      "columns": {
        "id": "Integer",
        "username": "String(80)",
        "email": "String(120)",
        "pw_hashed": "String(255)",
        "users_type_id": "Integer",
        "parent_id": "Integer",
        "referred_by_users_id": "Integer",
        "payee_id": "Integer",
        "name_first": "String(100)",
        "name_last": "String(100)",
        "name_display": "String(100)",
        "phone": "String(20)",
        "address_1": "String(255)",
        "address_2": "String(255)",
        "city": "String(100)",
        "state": "String(100)",
        "postal_zip": "String(20)",
        "country": "String(100)",
        "about_users": "Text",
        "avatar_url": "String(255)",
        "rating_limit": "String(20)",
        "timezone": "String(50)",
        "language_preference": "String(10)",
        "credit_balance": "Numeric(10, 2)",
        "total_storage_used_mb": "Integer",
        "is_active": "Boolean",
        "is_verified": "Boolean",
        "is_verified_email": "Boolean",
        "is_verified_phone": "Boolean",
        "preferences": "JSON",
        "new_episode_notification": "Boolean",
        "notification_settings": "JSON",
        "last_login_at": "DateTime",
        "failed_login_attempts": "Integer",
        "is_locked_out": "Boolean",
        "lockout_until": "DateTime",
        "password_reset_token": "String(100)",
        "password_reset_expiration": "DateTime",
        "created_at": "DateTime",
        "updated_at": "DateTime",
        "created_by": "Integer",
        "updated_by": "Integer"
      },
      "relationships": {
        "user_type": "UserType",
        "parent": "User",
        "children": "User",
        "sessions": "UserSession",
        "devices": "UserDevice",
        "notifications": "Notification",
        "actions": "UserAction"
      }
    },
    "UserSession": {
      "table_name": "users_sessions",
      "columns": {
        "id": "Integer",
        "user_id": "Integer",
        "session_token": "String(255)",
        "expires_at": "DateTime",
        "ip_address": "String(45)",
        "user_agent": "Text",
        "created_at": "DateTime",
        "last_activity": "DateTime"
      },
      "relationships": {
        "user": "User"
      }
    },
    "UserDevice": {
      "table_name": "users_devices",
      "columns": {
        "id": "Integer",
        "user_id": "Integer",
        "device_name": "String(100)",
        "device_type": "String(50)",
        "device_fingerprint": "String(255)",
        "last_active": "DateTime",
        "login_count": "Integer",
        "is_trusted": "Boolean",
        "is_blocked": "Boolean",
        "created_at": "DateTime"
      },
      "relationships": {
        "user": "User"
      }
    },
    "Notification": {
      "table_name": "notifications",
      "columns": {
        "id": "Integer",
        "user_id": "Integer",
        "title": "String(255)",
        "message": "Text",
        "notification_type": "String(50)",
        "is_read": "Boolean",
        "priority": "String(20)",
        "action_url": "String(500)",
        "action_data": "JSON",
        "created_at": "DateTime",
        "read_at": "DateTime"
      },
      "relationships": {
        "user": "User"
      }
    },
    "UserAction": {
      "table_name": "users_actions",
      "columns": {
        "id": "Integer",
        "users_id": "Integer",
        "action_type": "String(100)",
        "action_category": "String(50)",
        "action_data": "JSON",
        "ip_address": "String(45)",
        "user_agent": "Text",
        "target_type": "String(50)",
        "target_id": "Integer",
        "created_at": "DateTime"
      },
      "relationships": {
        "user": "User"
      }
    }
  }
}

# Documentation schema from markdown file
doc_schema = {
  "active_users_with_types": {
    "columns": {
      "id": "integer",
      "username": "character varying(100)",
      "email": "character varying(255)",
      "name_first": "character varying(100)",
      "name_last": "character varying(100)",
      "credit_balance": "integer",
      "is_active": "boolean",
      "created_at": "timestamp with time zone",
      "user_type_code": "character varying(50)",
      "user_type_name": "character varying(255)",
      "can_resell": "boolean"
    }
  },
  "api_keys": {
    "columns": {
      "id": "integer",
      "users_id": "integer",
      "key_name": "character varying(100)",
      "api_key": "character varying(255)",
      "api_secret": "character varying(255)",
      "permissions": "jsonb",
      "rate_limit_per_hour": "integer",
      "is_active": "boolean",
      "last_used_at": "timestamp with time zone",
      "expires_at": "timestamp with time zone",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer"
    }
  },
  "media_performers": {
    "columns": {
      "id": "integer",
      "media_id": "integer",
      "name": "character varying(255)",
      "character_name": "character varying(255)",
      "profile_path": "character varying(255)",
      "tmdb_id": "integer",
      "gender": "integer",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "content_reports": {
    "columns": {
      "id": "integer",
      "reported_by_users_id": "integer",
      "media_id": "integer",
      "report_type": "character varying(30)",
      "description": "text",
      "status": "character varying(20)",
      "admin_notes": "text",
      "resolved_by_users_id": "integer",
      "resolved_at": "timestamp with time zone",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone"
    }
  },
  "credit_packages": {
    "columns": {
      "id": "integer",
      "name": "character varying(100)",
      "description": "text",
      "credit_amount": "integer",
      "price_amount": "numeric",
      "currency": "character varying(3)",
      "bonus_credits": "integer",
      "is_active": "boolean",
      "sort_order": "integer",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "credit_transactions": {
    "columns": {
      "id": "integer",
      "users_id": "integer",
      "transaction_type": "character varying(20)",
      "amount": "integer",
      "balance_before": "integer",
      "balance_after": "integer",
      "description": "text",
      "reference_type": "character varying(50)",
      "reference_id": "integer",
      "payment_id": "integer",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "episodes": {
    "columns": {
      "id": "integer",
      "media_id": "integer",
      "episode_number": "integer",
      "name": "character varying(255)",
      "overview": "text",
      "season_number": "integer",
      "still_path": "character varying(255)",
      "air_date": "timestamp with time zone",
      "vote_average": "real",
      "vote_count": "integer",
      "rating": "character varying(255)",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "events": {
    "columns": {
      "id": "bigint",
      "events_type_id": "integer",
      "users_id": "integer",
      "session_id": "character varying(255)",
      "ip_address": "inet",
      "users_agent": "text",
      "event_data": "jsonb",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "events_types": {
    "columns": {
      "id": "integer",
      "code": "character varying(50)",
      "name": "character varying(100)",
      "description": "text",
      "is_tracked": "boolean",
      "retention_days": "integer",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "files": {
    "columns": {
      "id": "integer",
      "media_id": "integer",
      "episode_id": "integer",
      "path": "character varying(500)",
      "file_size": "bigint",
      "label": "character varying(255)",
      "original_filename": "character varying(500)",
      "content_type": "character varying(255)",
      "external_id": "character varying(255)",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "genres": {
    "columns": {
      "id": "integer",
      "tmdb_id": "integer",
      "name": "character varying(255)",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "invitations": {
    "columns": {
      "id": "integer",
      "inviter_users_id": "integer",
      "invited_email": "character varying(255)",
      "invitation_token": "character varying(255)",
      "status": "character varying(20)",
      "expires_at": "timestamp with time zone",
      "accepted_users_id": "integer",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "languages": {
    "columns": {
      "id": "integer",
      "code": "character varying(10)",
      "name": "character varying(50)",
      "native_name": "character varying(50)",
      "is_active": "boolean",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "media": {
    "columns": {
      "id": "integer",
      "users_id": "integer",
      "media_type_id": "integer",
      "title": "character varying(255)",
      "description": "text",
      "filename_original": "character varying(500)",
      "filename_stored": "character varying(500)",
      "file_path": "character varying(1000)",
      "file_size_bytes": "bigint",
      "file_size_mb": "numeric",
      "mime_type": "character varying(100)",
      "file_hash": "character varying(255)",
      "thumbnail_path": "character varying(1000)",
      "preview_path": "character varying(1000)",
      "metadata": "jsonb",
      "tags": "ARRAY",
      "is_public": "boolean",
      "is_featured": "boolean",
      "is_processed": "boolean",
      "processing_status": "character varying(20)",
      "download_count": "integer",
      "view_count": "integer",
      "like_count": "integer",
      "credit_cost": "integer",
      "expires_at": "timestamp with time zone",
      "added_date": "timestamp with time zone",
      "backdrop_path": "character varying(255)",
      "content_id": "integer",
      "content_type": "character varying(255)",
      "last_episode_air_date": "timestamp with time zone",
      "name": "character varying(255)",
      "original_language": "character varying(255)",
      "original_name": "character varying(255)",
      "overview": "text",
      "release_date": "timestamp with time zone",
      "runtime": "integer",
      "status": "character varying(255)",
      "still_path": "character varying(255)",
      "tagline": "character varying(255)",
      "tmdb_id": "integer",
      "total_episodes": "integer",
      "total_seasons": "integer",
      "trailer_id": "character varying(255)",
      "vote_average": "real",
      "vote_count": "integer",
      "trailer_url": "character varying(255)",
      "media_type_tmdb": "character varying(255)",
      "video_trailer_file_id": "integer",
      "imdb_id": "character varying(255)",
      "genre": "character varying(255)",
      "adult": "boolean",
      "min_age": "integer",
      "rating": "character varying(255)",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "media_categories": {
    "columns": {
      "id": "integer",
      "parent_id": "integer",
      "name": "character varying(100)",
      "slug": "character varying(100)",
      "description": "text",
      "is_active": "boolean",
      "sort_order": "integer",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "media_categories_assignments": {
    "columns": {
      "id": "integer",
      "media_id": "integer",
      "category_id": "integer",
      "created_at": "timestamp with time zone",
      "created_by": "integer"
    }
  },
  "media_genres": {
    "columns": {
      "id": "integer",
      "media_id": "integer",
      "genre_id": "integer",
      "created_at": "timestamp with time zone",
      "created_by": "integer"
    }
  },
  "media_quality_levels": {
    "columns": {
      "id": "integer",
      "media_id": "integer",
      "quality_name": "character varying(20)",
      "file_path": "character varying(1000)",
      "file_size_bytes": "bigint",
      "bitrate_kbps": "integer",
      "resolution_width": "integer",
      "resolution_height": "integer",
      "codec": "character varying(50)",
      "is_default": "boolean",
      "processing_status": "character varying(20)",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone"
    }
  },
  "media_subtitles": {
    "columns": {
      "id": "integer",
      "media_id": "integer",
      "language_id": "integer",
      "file_path": "character varying(1000)",
      "file_size_bytes": "integer",
      "mime_type": "character varying(100)",
      "is_default": "boolean",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "media_types": {
    "columns": {
      "id": "integer",
      "code": "character varying(50)",
      "name": "character varying(100)",
      "description": "text",
      "allowed_extensions": "ARRAY",
      "max_file_size_mb": "integer",
      "requires_processing": "boolean",
      "credit_cost": "integer",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "notifications": {
    "columns": {
      "id": "integer",
      "users_id": "integer",
      "notification_type": "character varying(50)",
      "title": "character varying(255)",
      "message": "text",
      "action_url": "character varying(500)",
      "is_read": "boolean",
      "is_sent": "boolean",
      "priority": "character varying(10)",
      "expires_at": "timestamp with time zone",
      "metadata": "jsonb",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer"
    }
  },
  "payment_methods": {
    "columns": {
      "id": "integer",
      "code": "character varying(50)",
      "name": "character varying(100)",
      "description": "text",
      "is_active": "boolean",
      "configuration": "jsonb",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "payments": {
    "columns": {
      "id": "integer",
      "users_id": "integer",
      "payment_method_id": "integer",
      "credit_package_id": "integer",
      "subscription_id": "integer",
      "payment_status": "character varying(20)",
      "amount": "numeric",
      "currency": "character varying(3)",
      "credits_purchased": "integer",
      "external_transaction_id": "character varying(255)",
      "gateway_response": "jsonb",
      "processed_at": "timestamp with time zone",
      "failed_reason": "text",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "playlists": {
    "columns": {
      "id": "integer",
      "users_id": "integer",
      "name": "character varying(255)",
      "description": "text",
      "is_public": "boolean",
      "thumbnail_url": "character varying(1000)",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "playlists_media_items": {
    "columns": {
      "id": "integer",
      "playlist_id": "integer",
      "media_id": "integer",
      "sort_order": "integer",
      "added_at": "timestamp with time zone",
      "added_by": "integer"
    }
  },
  "referral_codes": {
    "columns": {
      "id": "integer",
      "code": "character varying(50)",
      "referrer_users_id": "integer",
      "referred_users_id": "integer",
      "usage_limit": "integer",
      "current_uses": "integer",
      "reward_type": "character varying(20)",
      "reward_value": "integer",
      "expires_at": "timestamp with time zone",
      "is_active": "boolean",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "resellers_assets": {
    "columns": {
      "id": "integer",
      "reseller_id": "integer",
      "asset_type": "character varying(20)",
      "asset_name": "character varying(255)",
      "file_path": "character varying(500)",
      "file_size_bytes": "integer",
      "mime_type": "character varying(100)",
      "is_active": "boolean",
      "sort_order": "integer",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "resellers_commissions": {
    "columns": {
      "id": "integer",
      "reseller_users_id": "integer",
      "customer_users_id": "integer",
      "transaction_type": "character varying(50)",
      "reference_id": "integer",
      "commission_rate": "numeric",
      "base_amount": "numeric",
      "commission_amount": "numeric",
      "currency": "character varying(3)",
      "status": "character varying(20)",
      "notes": "text",
      "approved_at": "timestamp with time zone",
      "paid_at": "timestamp with time zone",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "resellers_details": {
    "columns": {
      "id": "integer",
      "users_id": "integer",
      "users_counter": "integer",
      "users_max": "integer",
      "business_name": "character varying(255)",
      "tax_id": "character varying(50)",
      "website_url": "character varying(500)",
      "commission_rate": "numeric",
      "min_payout_amount": "numeric",
      "payout_method": "character varying(50)",
      "payout_details": "jsonb",
      "total_referrals": "integer",
      "total_earnings": "numeric",
      "pending_earnings": "numeric",
      "paid_earnings": "numeric",
      "is_approved": "boolean",
      "approval_date": "timestamp with time zone",
      "notes": "text",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "resellers_settings": {
    "columns": {
      "id": "integer",
      "reseller_id": "integer",
      "setting_key": "character varying(100)",
      "setting_value": "text",
      "setting_type": "character varying(20)",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "subscriptions": {
    "columns": {
      "id": "integer",
      "users_id": "integer",
      "subscriptions_plan_id": "integer",
      "start_date": "timestamp with time zone",
      "end_date": "timestamp with time zone",
      "status": "character varying(20)",
      "auto_renew": "boolean",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "subscriptions_history": {
    "columns": {
      "id": "integer",
      "subscription_id": "integer",
      "users_id": "integer",
      "subscriptions_plan_id": "integer",
      "action_type": "character varying(20)",
      "old_status": "character varying(20)",
      "new_status": "character varying(20)",
      "old_end_date": "timestamp with time zone",
      "new_end_date": "timestamp with time zone",
      "reason": "text",
      "created_at": "timestamp with time zone",
      "created_by": "integer"
    }
  },
  "subscriptions_plans": {
    "columns": {
      "id": "integer",
      "name": "character varying(100)",
      "description": "text",
      "price": "numeric",
      "currency": "character varying(3)",
      "duration_days": "integer",
      "max_storage_mb": "integer",
      "max_uploads": "integer",
      "features": "jsonb",
      "is_active": "boolean",
      "sort_order": "integer",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "support_tickets": {
    "columns": {
      "id": "integer",
      "users_id": "integer",
      "assigned_to_users_id": "integer",
      "subject": "character varying(255)",
      "description": "text",
      "status": "character varying(20)",
      "priority": "character varying(10)",
      "category": "character varying(50)",
      "last_activity_at": "timestamp with time zone",
      "closed_at": "timestamp with time zone",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "system_settings": {
    "columns": {
      "id": "integer",
      "setting_key": "character varying(100)",
      "setting_value": "text",
      "setting_type": "character varying(20)",
      "description": "text",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "tickets_messages": {
    "columns": {
      "id": "integer",
      "ticket_id": "integer",
      "users_id": "integer",
      "message": "text",
      "is_internal": "boolean",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "transactions": {
    "columns": {
      "id": "integer",
      "sender_users_id": "integer",
      "receiver_users_id": "integer",
      "transactions_type_id": "integer",
      "amount": "numeric",
      "currency": "character varying(3)",
      "payment_method_id": "integer",
      "status": "character varying(20)",
      "external_transaction_id": "character varying(255)",
      "notes": "text",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "transactions_types": {
    "columns": {
      "id": "integer",
      "code": "character varying(50)",
      "name": "character varying(100)",
      "description": "text",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "tv_channels": {
    "columns": {
      "id": "integer",
      "name": "character varying(255)",
      "channel_number": "integer",
      "logo_url": "character varying(500)",
      "stream_url": "character varying(1000)",
      "description": "text",
      "category_id": "integer",
      "is_active": "boolean",
      "geo_restriction": "jsonb",
      "requires_subscriptions_plan_id": "integer",
      "credit_cost": "integer",
      "metadata": "jsonb",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  },
  "user_media_affinity": {
    "columns": {
      "id": "integer",
      "user_id": "integer",
      "genre_id": "integer",
      "affinity_score": "double precision",
      "updated_at": "timestamp without time zone"
    }
  },
  "users": {
    "columns": {
      "id": "integer",
      "users_type_id": "integer",
      "parent_id": "integer",
      "referred_by_users_id": "integer",
      "payee_id": "integer",
      "username": "character varying(100)",
      "email": "character varying(255)",
      "pw_hashed": "character varying(255)",
      "name_first": "character varying(100)",
      "name_last": "character varying(100)",
      "name_display": "character varying(150)",
      "phone": "character varying(20)",
      "address_1": "character varying(255)",
      "address_2": "character varying(255)",
      "city": "character varying(100)",
      "state": "character varying(100)",
      "postal_zip": "character varying(20)",
      "country": "character varying(100)",
      "about_users": "text",
      "avatar_url": "character varying(500)",
      "rating_limit": "character varying(10)",
      "credit_balance": "integer",
      "total_storage_used_mb": "integer",
      "is_active": "boolean",
      "is_verified": "boolean",
      "is_verified_email": "boolean",
      "is_verified_phone": "boolean",
      "preferences": "jsonb",
      "new_episode_notification": "boolean",
      "notification_settings": "jsonb",
      "timezone": "character varying(50)",
      "language_preference": "character varying(10)",
      "last_login_at": "timestamp with time zone",
      "failed_login_attempts": "integer",
      "is_locked_out": "boolean",
      "lockout_until": "timestamp with time zone",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer",
      "password_reset_token": "character varying(255)",
      "password_reset_expiration": "timestamp with time zone"
    }
  },
  "users_actions": {
    "columns": {
      "id": "integer",
      "users_id": "integer",
      "action_type": "character varying(100)",
      "action_category": "character varying(50)",
      "action_data": "jsonb",
      "ip_address": "character varying(45)",
      "user_agent": "text",
      "target_type": "character varying(50)",
      "target_id": "integer",
      "created_at": "timestamp with time zone"
    }
  },
  "users_devices": {
    "columns": {
      "id": "integer",
      "users_id": "integer",
      "device_fingerprint": "character varying(255)",
      "device_name": "character varying(255)",
      "device_type": "character varying(50)",
      "browser_info": "jsonb",
      "is_trusted": "boolean",
      "last_used_at": "timestamp with time zone",
      "ip_address": "inet",
      "location_info": "jsonb",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone"
    }
  },
  "users_favorites": {
    "columns": {
      "id": "integer",
      "users_id": "integer",
      "media_id": "integer",
      "favorite_type": "character varying(20)",
      "notes": "text",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone"
    }
  },
  "users_media_affinity": {
    "columns": {
      "id": "bigint",
      "users_id": "integer",
      "media_id": "integer",
      "affinity_score": "real",
      "affinity_type": "character varying(50)",
      "explanation": "text",
      "last_calculated_at": "timestamp with time zone",
      "metadata": "jsonb",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone"
    }
  },
  "users_media_history": {
    "columns": {
      "id": "bigint",
      "users_id": "integer",
      "media_id": "integer",
      "action_type": "character varying(20)",
      "playback_position_seconds": "integer",
      "completion_percentage": "integer",
      "credits_spent": "integer",
      "quality_level": "character varying(20)",
      "device_type": "character varying(50)",
      "ip_address": "inet",
      "device_info": "jsonb",
      "updated_at": "timestamp with time zone",
      "created_at": "timestamp with time zone"
    }
  },
  "users_ratings": {
    "columns": {
      "id": "integer",
      "users_id": "integer",
      "media_id": "integer",
      "rating": "integer",
      "review_text": "text",
      "is_public": "boolean",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone"
    }
  },
  "users_referral_earnings": {
    "columns": {
      "id": "integer",
      "referrer_users_id": "integer",
      "referred_users_id": "integer",
      "referral_code_id": "integer",
      "earning_type": "character varying(30)",
      "amount": "numeric",
      "currency": "character varying(3)",
      "credits_awarded": "integer",
      "reference_transaction_id": "integer",
      "status": "character varying(20)",
      "paid_at": "timestamp with time zone",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone"
    }
  },
  "users_sessions": {
    "columns": {
      "id": "integer",
      "users_id": "integer",
      "session_token": "character varying(255)",
      "device_info": "jsonb",
      "ip_address": "inet",
      "is_active": "boolean",
      "last_activity_at": "timestamp with time zone",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone"
    }
  },
  "users_types": {
    "columns": {
      "id": "integer",
      "code": "character varying(50)",
      "name": "character varying(255)",
      "description": "text",
      "max_uploads": "integer",
      "max_storage_mb": "integer",
      "can_resell": "boolean",
      "is_default": "boolean",
      "created_at": "timestamp with time zone",
      "updated_at": "timestamp with time zone",
      "created_by": "integer",
      "updated_by": "integer"
    }
  }
}

if __name__ == "__main__":
    discrepancies = compare_schemas(model_schema, doc_schema)
    
    # Save discrepancies to a JSON file
    with open("schema_discrepancies.json", "w") as f:
        json.dump(discrepancies, f, indent=2)
    
    print("Schema comparison complete. Discrepancies saved to schema_discrepancies.json")