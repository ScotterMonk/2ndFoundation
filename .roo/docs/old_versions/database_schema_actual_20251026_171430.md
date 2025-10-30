# Database Schema Overview

*Last updated: 2025-10-26 11:39:18*

## Tables

### view: active_users_with_types

**Columns:**
- `id`: integer NULL
- `username`: character varying(100) NULL
- `email`: character varying(255) NULL
- `name_first`: character varying(100) NULL
- `name_last`: character varying(100) NULL
- `credit_balance`: integer NULL
- `is_active`: boolean NULL
- `created_at`: timestamp with time zone NULL
- `user_type_code`: character varying(50) NULL
- `user_type_name`: character varying(255) NULL
- `can_resell`: boolean NULL

### api_keys

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `users_id`: integer NOT NULL
- `key_name`: character varying(100) NOT NULL
- `api_key`: character varying(255) NOT NULL
- `api_secret`: character varying(255) NULL
- `permissions`: jsonb NOT NULL
- `rate_limit_per_hour`: integer NOT NULL
- `is_active`: boolean NOT NULL
- `last_used_at`: timestamp with time zone NULL
- `expires_at`: timestamp with time zone NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `users_id` -> `users.id`

### content_reports

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `reported_by_users_id`: integer NULL
- `media_id`: integer NOT NULL
- `report_type`: character varying(30) NOT NULL
- `description`: text NOT NULL
- `status`: character varying(20) NOT NULL
- `admin_notes`: text NULL
- `resolved_by_users_id`: integer NULL
- `resolved_at`: timestamp with time zone NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL

**Foreign Keys:**
- `media_id` -> `media.id`
- `reported_by_users_id` -> `users.id`
- `resolved_by_users_id` -> `users.id`

### credit_packages

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `name`: character varying(100) NOT NULL
- `description`: text NULL
- `credit_amount`: integer NOT NULL
- `price_amount`: numeric(15,2) NOT NULL
- `currency`: character varying(3) NOT NULL
- `bonus_credits`: integer NOT NULL
- `is_active`: boolean NOT NULL
- `sort_order`: integer NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `updated_by` -> `users.id`

### credit_transactions

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `users_id`: integer NOT NULL
- `transaction_type`: character varying(20) NOT NULL
- `amount`: integer NOT NULL
- `balance_before`: integer NOT NULL
- `balance_after`: integer NOT NULL
- `description`: text NULL
- `reference_type`: character varying(50) NULL
- `reference_id`: integer NULL
- `payment_id`: integer NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `payment_id` -> `payments.id`
- `updated_by` -> `users.id`
- `users_id` -> `users.id`

### directors

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `name`: character varying NULL
- `description`: text NULL
- `profile_path`: character varying NULL
- `tmdb_id`: integer NULL
- `imdb_id`: character varying NULL
- `gender`: integer NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

### episodes

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `media_id`: integer NOT NULL
- `episode_number`: integer NULL
- `name`: character varying(255) NULL
- `overview`: text NULL
- `season_number`: integer NULL
- `still_path`: character varying(255) NULL
- `air_date`: timestamp with time zone NULL
- `vote_average`: real NULL
- `vote_count`: integer NULL
- `user_score`: character varying(255) NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `media_id` -> `media.id`
- `updated_by` -> `users.id`

### events

**Primary Key:** id

**Columns:**
- `id`: bigint NOT NULL
- `events_type_id`: integer NOT NULL
- `users_id`: integer NULL
- `session_id`: character varying(255) NULL
- `ip_address`: inet NULL
- `users_agent`: text NULL
- `event_data`: jsonb NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `events_type_id` -> `events_types.id`
- `updated_by` -> `users.id`
- `users_id` -> `users.id`

### events_types

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `code`: character varying(50) NOT NULL
- `name`: character varying(100) NOT NULL
- `description`: text NULL
- `is_tracked`: boolean NOT NULL
- `retention_days`: integer NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `updated_by` -> `users.id`

### files

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `media_id`: integer NULL
- `episode_id`: integer NULL
- `path`: character varying(500) NOT NULL
- `file_size`: bigint NULL
- `label`: character varying(255) NULL
- `original_filename`: character varying(500) NULL
- `content_type`: character varying(255) NULL
- `external_id`: character varying(255) NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `episode_id` -> `episodes.id`
- `media_id` -> `media.id`
- `updated_by` -> `users.id`

### genres

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `name`: character varying(255) NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `updated_by` -> `users.id`

### invitations

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `inviter_users_id`: integer NOT NULL
- `invited_email`: character varying(255) NOT NULL
- `invitation_token`: character varying(255) NOT NULL
- `status`: character varying(20) NOT NULL
- `expires_at`: timestamp with time zone NOT NULL
- `accepted_users_id`: integer NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `accepted_users_id` -> `users.id`
- `created_by` -> `users.id`
- `inviter_users_id` -> `users.id`
- `updated_by` -> `users.id`

### languages

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `code`: character varying(10) NOT NULL
- `name`: character varying(50) NOT NULL
- `native_name`: character varying(50) NULL
- `is_active`: boolean NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `updated_by` -> `users.id`

### media

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `users_id`: integer NOT NULL
- `media_type_id`: integer NOT NULL
- `title`: character varying NOT NULL
- `description`: text NULL
- `imdb_id`: character varying NULL
- `imdb_rating`: numeric NULL
- `tmdb_id`: integer NULL
- `tmdb_rating`: numeric NULL
- `tmdb_media_type`: character varying NULL
- `tvdb_id`: integer NULL
- `tvdb_rating`: numeric NULL
- `other_id`: integer NULL
- `other_rating`: numeric NULL
- `user_score`: numeric NULL
- `resolution`: character varying NULL
- `filename_original`: character varying NOT NULL
- `filename_stored`: character varying NOT NULL
- `file_path`: character varying NOT NULL
- `file_size_bytes`: bigint NOT NULL
- `mime_type`: character varying NOT NULL
- `file_hash`: character varying NULL
- `thumbnail_path`: character varying NULL
- `preview_path`: character varying NULL
- `metadata`: jsonb NOT NULL
- `tags`: character varying NULL
- `is_public`: boolean NOT NULL
- `is_featured`: boolean NOT NULL
- `is_processed`: boolean NOT NULL
- `processing_status`: character varying NOT NULL
- `download_count`: integer NOT NULL
- `view_count`: integer NOT NULL
- `like_count`: integer NOT NULL
- `credit_cost`: integer NOT NULL
- `expires_at`: timestamp with time zone NULL
- `added_date`: timestamp with time zone NULL
- `backdrop_path`: character varying NULL
- `content_id`: integer NULL
- `content_type`: character varying NULL
- `last_episode_air_date`: timestamp with time zone NULL
- `name`: character varying NULL
- `original_language`: character varying NULL
- `original_name`: character varying NULL
- `overview`: text NULL
- `release_date`: timestamp with time zone NULL
- `runtime`: integer NULL
- `status`: character varying NULL
- `still_path`: character varying NULL
- `tagline`: character varying NULL
- `total_episodes`: integer NULL
- `total_seasons`: integer NULL
- `trailer_id`: character varying NULL
- `vote_average`: real NULL
- `vote_count`: integer NULL
- `trailer_url`: character varying NULL
- `video_trailer_file_id`: integer NULL
- `genre`: character varying NULL
- `adult`: boolean NOT NULL
- `min_age`: integer NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL
- `title_alternate`: character varying NULL
- `title_for_sorting`: character varying NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `media_type_id` -> `media_types.id`
- `updated_by` -> `users.id`
- `users_id` -> `users.id`
- `video_trailer_file_id` -> `files.id`

### media_backup

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `users_id`: integer NOT NULL
- `media_type_id`: integer NOT NULL
- `title`: character varying(255) NOT NULL
- `description`: text NULL
- `filename_original`: character varying(500) NOT NULL
- `filename_stored`: character varying(500) NOT NULL
- `file_path`: character varying(1000) NOT NULL
- `file_size_bytes`: bigint NOT NULL
- `mime_type`: character varying(100) NOT NULL
- `file_hash`: character varying(255) NULL
- `thumbnail_path`: character varying(1000) NULL
- `preview_path`: character varying(1000) NULL
- `metadata`: jsonb NOT NULL
- `tags`: _text[] NULL
- `is_public`: boolean NOT NULL
- `is_featured`: boolean NOT NULL
- `is_processed`: boolean NOT NULL
- `processing_status`: character varying(20) NOT NULL
- `download_count`: integer NOT NULL
- `view_count`: integer NOT NULL
- `like_count`: integer NOT NULL
- `credit_cost`: integer NOT NULL
- `expires_at`: timestamp with time zone NULL
- `added_date`: timestamp with time zone NULL
- `backdrop_path`: character varying(255) NULL
- `content_id`: integer NULL
- `content_type`: character varying(255) NULL
- `last_episode_air_date`: timestamp with time zone NULL
- `name`: character varying(255) NULL
- `original_language`: character varying(255) NULL
- `original_name`: character varying(255) NULL
- `overview`: text NULL
- `release_date`: timestamp with time zone NULL
- `runtime`: integer NULL
- `status`: character varying(255) NULL
- `still_path`: character varying(255) NULL
- `tagline`: character varying(255) NULL
- `tmdb_id`: integer NULL
- `total_episodes`: integer NULL
- `total_seasons`: integer NULL
- `trailer_id`: character varying(255) NULL
- `vote_average`: real NULL
- `vote_count`: integer NULL
- `trailer_url`: character varying(255) NULL
- `tmdb_media_type`: character varying(255) NULL
- `video_trailer_file_id`: integer NULL
- `imdb_id`: character varying(255) NULL
- `genre`: character varying(255) NULL
- `adult`: boolean NOT NULL
- `min_age`: integer NOT NULL
- `user_score`: character varying(255) NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL
- `tvdb_id`: integer NULL
- `tmdb_rating`: numeric NULL
- `imdb_rating`: numeric NULL

### media_categories

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `parent_id`: integer NULL
- `name`: character varying(100) NOT NULL
- `slug`: character varying(100) NOT NULL
- `description`: text NULL
- `is_active`: boolean NOT NULL
- `sort_order`: integer NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `parent_id` -> `media_categories.id`
- `updated_by` -> `users.id`

### media_categories_assignments

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `media_id`: integer NOT NULL
- `category_id`: integer NOT NULL
- `created_at`: timestamp with time zone NULL
- `created_by`: integer NULL

**Foreign Keys:**
- `category_id` -> `media_categories.id`
- `created_by` -> `users.id`
- `media_id` -> `media.id`

### media_directors

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `media_id`: integer NULL
- `director_id`: integer NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `director_id` -> `directors.id`
- `media_id` -> `media.id`
- `updated_by` -> `users.id`

### media_genres

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `media_id`: integer NOT NULL
- `genre_id`: integer NOT NULL
- `created_at`: timestamp with time zone NULL
- `created_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `genre_id` -> `genres.id`
- `media_id` -> `media.id`

### media_ignore

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `imdb_id`: character varying NULL
- `media_id`: integer NULL
- `other_id`: character varying NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

### media_performers

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `media_id`: integer NOT NULL
- `performer_id`: integer NOT NULL
- `character_name`: character varying NULL
- `gender`: integer NULL
- `created_at`: timestamp with time zone NOT NULL
- `updated_at`: timestamp with time zone NOT NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `media_id` -> `media.id`

### media_quality_levels

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `media_id`: integer NOT NULL
- `quality_name`: character varying(20) NOT NULL
- `file_path`: character varying(1000) NOT NULL
- `file_size_bytes`: bigint NOT NULL
- `bitrate_kbps`: integer NULL
- `resolution_width`: integer NULL
- `resolution_height`: integer NULL
- `codec`: character varying(50) NULL
- `is_default`: boolean NOT NULL
- `processing_status`: character varying(20) NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL

**Foreign Keys:**
- `media_id` -> `media.id`

### media_subtitles

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `media_id`: integer NOT NULL
- `language_id`: integer NOT NULL
- `file_path`: character varying(1000) NOT NULL
- `file_size_bytes`: integer NULL
- `mime_type`: character varying(100) NULL
- `is_default`: boolean NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `language_id` -> `languages.id`
- `media_id` -> `media.id`
- `updated_by` -> `users.id`

### media_types

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `code`: character varying(50) NOT NULL
- `name`: character varying(50) NOT NULL
- `description`: text NULL
- `allowed_extensions`: _text[] NULL
- `max_file_size_mb`: integer NULL
- `requires_processing`: boolean NOT NULL
- `credit_cost`: integer NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL
- `codes_imdb`: character varying NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `updated_by` -> `users.id`

### notifications

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `users_id`: integer NOT NULL
- `notification_type`: character varying(50) NOT NULL
- `title`: character varying(255) NOT NULL
- `message`: text NOT NULL
- `action_url`: character varying(500) NULL
- `is_read`: boolean NOT NULL
- `is_sent`: boolean NOT NULL
- `priority`: character varying(10) NOT NULL
- `expires_at`: timestamp with time zone NULL
- `metadata`: jsonb NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `users_id` -> `users.id`

### payment_methods

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `code`: character varying(50) NOT NULL
- `name`: character varying(100) NOT NULL
- `description`: text NULL
- `is_active`: boolean NOT NULL
- `configuration`: jsonb NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `updated_by` -> `users.id`

### payments

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `users_id`: integer NOT NULL
- `payment_method_id`: integer NOT NULL
- `credit_package_id`: integer NULL
- `subscription_id`: integer NULL
- `payment_status`: character varying(20) NOT NULL
- `amount`: numeric(15,2) NOT NULL
- `currency`: character varying(3) NOT NULL
- `credits_purchased`: integer NULL
- `external_transaction_id`: character varying(255) NULL
- `gateway_response`: jsonb NOT NULL
- `processed_at`: timestamp with time zone NULL
- `failed_reason`: text NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `credit_package_id` -> `credit_packages.id`
- `payment_method_id` -> `payment_methods.id`
- `subscription_id` -> `subscriptions.id`
- `updated_by` -> `users.id`
- `users_id` -> `users.id`

### performers

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `name`: character varying NULL
- `imdb_cast_id`: character varying NULL
- `profile_path`: character varying NULL
- `tmdb_id`: integer NULL
- `gender`: integer NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

### playlists

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `users_id`: integer NOT NULL
- `name`: character varying(255) NOT NULL
- `description`: text NULL
- `is_public`: boolean NOT NULL
- `thumbnail_url`: character varying(1000) NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `updated_by` -> `users.id`
- `users_id` -> `users.id`

### playlists_media_items

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `playlist_id`: integer NOT NULL
- `media_id`: integer NOT NULL
- `sort_order`: integer NOT NULL
- `added_at`: timestamp with time zone NULL
- `added_by`: integer NULL

**Foreign Keys:**
- `added_by` -> `users.id`
- `media_id` -> `media.id`
- `playlist_id` -> `playlists.id`

### referral_codes

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `code`: character varying(50) NOT NULL
- `referrer_users_id`: integer NOT NULL
- `referred_users_id`: integer NULL
- `usage_limit`: integer NOT NULL
- `current_uses`: integer NOT NULL
- `reward_type`: character varying(20) NULL
- `reward_value`: integer NULL
- `expires_at`: timestamp with time zone NULL
- `is_active`: boolean NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `referred_users_id` -> `users.id`
- `referrer_users_id` -> `users.id`
- `updated_by` -> `users.id`

### resellers_assets

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `reseller_id`: integer NOT NULL
- `asset_type`: character varying(20) NOT NULL
- `asset_name`: character varying(255) NOT NULL
- `file_path`: character varying(500) NOT NULL
- `file_size_bytes`: integer NULL
- `mime_type`: character varying(100) NULL
- `is_active`: boolean NOT NULL
- `sort_order`: integer NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `reseller_id` -> `users.id`
- `updated_by` -> `users.id`

### resellers_commissions

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `reseller_users_id`: integer NOT NULL
- `customer_users_id`: integer NOT NULL
- `transaction_type`: character varying(50) NOT NULL
- `reference_id`: integer NULL
- `commission_rate`: numeric(5,4) NOT NULL
- `base_amount`: numeric(15,2) NOT NULL
- `commission_amount`: numeric(15,2) NOT NULL
- `currency`: character varying(3) NOT NULL
- `status`: character varying(20) NOT NULL
- `notes`: text NULL
- `approved_at`: timestamp with time zone NULL
- `paid_at`: timestamp with time zone NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `customer_users_id` -> `users.id`
- `reseller_users_id` -> `users.id`
- `updated_by` -> `users.id`

### resellers_details

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `users_id`: integer NOT NULL
- `users_counter`: integer NOT NULL
- `users_max`: integer NOT NULL
- `business_name`: character varying(255) NULL
- `tax_id`: character varying(50) NULL
- `website_url`: character varying(500) NULL
- `commission_rate`: numeric(5,4) NOT NULL
- `min_payout_amount`: numeric(15,2) NOT NULL
- `payout_method`: character varying(50) NULL
- `payout_details`: jsonb NOT NULL
- `total_referrals`: integer NOT NULL
- `total_earnings`: numeric(15,2) NOT NULL
- `pending_earnings`: numeric(15,2) NOT NULL
- `paid_earnings`: numeric(15,2) NOT NULL
- `is_approved`: boolean NOT NULL
- `approval_date`: timestamp with time zone NULL
- `notes`: text NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `updated_by` -> `users.id`
- `users_id` -> `users.id`

### resellers_settings

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `reseller_id`: integer NOT NULL
- `setting_key`: character varying(100) NOT NULL
- `setting_value`: text NULL
- `setting_type`: character varying(20) NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `reseller_id` -> `users.id`
- `updated_by` -> `users.id`

### subscriptions

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `users_id`: integer NOT NULL
- `subscriptions_plan_id`: integer NOT NULL
- `start_date`: timestamp with time zone NOT NULL
- `end_date`: timestamp with time zone NOT NULL
- `status`: character varying(20) NOT NULL
- `auto_renew`: boolean NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `subscriptions_plan_id` -> `subscriptions_plans.id`
- `updated_by` -> `users.id`
- `users_id` -> `users.id`

### subscriptions_history

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `subscription_id`: integer NOT NULL
- `users_id`: integer NOT NULL
- `subscriptions_plan_id`: integer NOT NULL
- `action_type`: character varying(20) NOT NULL
- `old_status`: character varying(20) NULL
- `new_status`: character varying(20) NULL
- `old_end_date`: timestamp with time zone NULL
- `new_end_date`: timestamp with time zone NULL
- `reason`: text NULL
- `created_at`: timestamp with time zone NULL
- `created_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `subscription_id` -> `subscriptions.id`
- `subscriptions_plan_id` -> `subscriptions_plans.id`
- `users_id` -> `users.id`

### subscriptions_plans

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `name`: character varying(100) NOT NULL
- `description`: text NULL
- `price`: numeric(15,2) NOT NULL
- `currency`: character varying(3) NOT NULL
- `duration_days`: integer NOT NULL
- `max_storage_mb`: integer NULL
- `max_uploads`: integer NULL
- `features`: jsonb NOT NULL
- `is_active`: boolean NOT NULL
- `sort_order`: integer NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `updated_by` -> `users.id`

### support_tickets

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `users_id`: integer NOT NULL
- `assigned_to_users_id`: integer NULL
- `subject`: character varying(255) NOT NULL
- `description`: text NULL
- `status`: character varying(20) NOT NULL
- `priority`: character varying(10) NOT NULL
- `category`: character varying(50) NULL
- `last_activity_at`: timestamp with time zone NULL
- `closed_at`: timestamp with time zone NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `assigned_to_users_id` -> `users.id`
- `created_by` -> `users.id`
- `updated_by` -> `users.id`
- `users_id` -> `users.id`

### system_settings

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `setting_key`: character varying(100) NOT NULL
- `setting_value`: text NULL
- `setting_type`: character varying(20) NOT NULL
- `description`: text NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

### tickets_messages

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `ticket_id`: integer NOT NULL
- `users_id`: integer NOT NULL
- `message`: text NOT NULL
- `is_internal`: boolean NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `ticket_id` -> `support_tickets.id`
- `updated_by` -> `users.id`
- `users_id` -> `users.id`

### transactions

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `sender_users_id`: integer NULL
- `receiver_users_id`: integer NULL
- `transactions_type_id`: integer NOT NULL
- `amount`: numeric(15,2) NOT NULL
- `currency`: character varying(3) NOT NULL
- `payment_method_id`: integer NULL
- `status`: character varying(20) NOT NULL
- `external_transaction_id`: character varying(255) NULL
- `notes`: text NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `payment_method_id` -> `payment_methods.id`
- `receiver_users_id` -> `users.id`
- `sender_users_id` -> `users.id`
- `transactions_type_id` -> `transactions_types.id`
- `updated_by` -> `users.id`

### transactions_types

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `code`: character varying(50) NOT NULL
- `name`: character varying(100) NOT NULL
- `description`: text NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `updated_by` -> `users.id`

### tv_channels

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `name`: character varying(255) NOT NULL
- `channel_number`: integer NULL
- `logo_url`: character varying(500) NULL
- `stream_url`: character varying(1000) NOT NULL
- `description`: text NULL
- `category_id`: integer NULL
- `is_active`: boolean NOT NULL
- `geo_restriction`: jsonb NOT NULL
- `requires_subscriptions_plan_id`: integer NULL
- `credit_cost`: integer NOT NULL
- `metadata`: jsonb NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `category_id` -> `media_categories.id`
- `created_by` -> `users.id`
- `requires_subscriptions_plan_id` -> `subscriptions_plans.id`
- `updated_by` -> `users.id`

### user_media_affinity

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `user_id`: integer NOT NULL
- `genre_id`: integer NOT NULL
- `affinity_score`: double precision NOT NULL
- `updated_at`: timestamp without time zone NOT NULL

**Foreign Keys:**
- `genre_id` -> `genres.id`
- `user_id` -> `users.id`

### users

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `users_type_id`: integer NOT NULL
- `parent_id`: integer NULL
- `referred_by_users_id`: integer NULL
- `payee_id`: integer NULL
- `username`: character varying(100) NOT NULL
- `email`: character varying(255) NOT NULL
- `pw_hashed`: character varying(255) NOT NULL
- `name_first`: character varying(100) NULL
- `name_last`: character varying(100) NULL
- `name_display`: character varying(150) NULL
- `phone`: character varying(20) NULL
- `address_1`: character varying(255) NULL
- `address_2`: character varying(255) NULL
- `city`: character varying(100) NULL
- `state`: character varying(100) NULL
- `postal_zip`: character varying(20) NULL
- `country`: character varying(100) NULL
- `about_users`: text NULL
- `avatar_url`: character varying(500) NULL
- `user_score_limit`: character varying(10) NULL
- `credit_balance`: integer NOT NULL
- `total_storage_used_mb`: integer NOT NULL
- `is_active`: boolean NOT NULL
- `is_verified`: boolean NOT NULL
- `is_verified_email`: boolean NOT NULL
- `is_verified_phone`: boolean NOT NULL
- `preferences`: jsonb NOT NULL
- `new_episode_notification`: boolean NOT NULL
- `notification_settings`: jsonb NOT NULL
- `timezone`: character varying(50) NULL
- `language_preference`: character varying(10) NULL
- `last_login_at`: timestamp with time zone NULL
- `failed_login_attempts`: integer NOT NULL
- `is_locked_out`: boolean NOT NULL
- `lockout_until`: timestamp with time zone NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL
- `password_reset_token`: character varying(255) NULL
- `password_reset_expiration`: timestamp with time zone NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `parent_id` -> `users.id`
- `payee_id` -> `users.id`
- `referred_by_users_id` -> `users.id`
- `updated_by` -> `users.id`
- `users_type_id` -> `users_types.id`

### users_actions

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `users_id`: integer NOT NULL
- `action_type`: character varying(50) NOT NULL
- `target_type`: character varying(50) NULL
- `target_id`: integer NULL
- `action_data`: jsonb NOT NULL
- `ip_address`: inet NULL
- `users_agent`: text NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL
- `action_category`: character varying(50) NOT NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `updated_by` -> `users.id`
- `users_id` -> `users.id`

### users_devices

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `users_id`: integer NOT NULL
- `device_fingerprint`: character varying(255) NOT NULL
- `device_name`: character varying(255) NULL
- `device_type`: character varying(50) NULL
- `browser_info`: jsonb NOT NULL
- `is_trusted`: boolean NOT NULL
- `last_used_at`: timestamp with time zone NULL
- `ip_address`: inet NULL
- `location_info`: jsonb NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL

**Foreign Keys:**
- `users_id` -> `users.id`

### users_faves_directors

**Columns:**
- `id`: integer NOT NULL
- `user_id`: integer NULL
- `director_id`: integer NULL
- `weight`: integer NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `director_id` -> `directors.id`
- `user_id` -> `users.id`

### users_faves_genres

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `user_id`: integer NOT NULL
- `genre_id`: integer NOT NULL
- `weight`: integer NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `genre_id` -> `genres.id`
- `updated_by` -> `users.id`
- `user_id` -> `users.id`

### users_faves_performers

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `user_id`: integer NULL
- `performer_id`: integer NULL
- `weight`: integer NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `performer_id` -> `performers.id`
- `updated_by` -> `users.id`
- `user_id` -> `users.id`

### users_favorites

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `users_id`: integer NULL
- `media_id`: integer NULL
- `favorite_type`: character varying(20) NULL
- `notes`: text NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL

**Foreign Keys:**
- `media_id` -> `media.id`
- `users_id` -> `users.id`

### users_media_affinity

**Primary Key:** id

**Columns:**
- `id`: bigint NOT NULL
- `users_id`: integer NOT NULL
- `media_id`: integer NOT NULL
- `affinity_score`: real NOT NULL
- `affinity_type`: character varying(50) NOT NULL
- `explanation`: text NULL
- `last_calculated_at`: timestamp with time zone NULL
- `affinity_metadata`: jsonb NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL

**Foreign Keys:**
- `media_id` -> `media.id`
- `users_id` -> `users.id`

### users_media_history

**Primary Key:** id

**Columns:**
- `id`: bigint NOT NULL
- `users_id`: integer NOT NULL
- `media_id`: integer NOT NULL
- `action_type`: character varying(20) NOT NULL
- `playback_position_seconds`: integer NOT NULL
- `completion_percentage`: integer NOT NULL
- `credits_spent`: integer NOT NULL
- `quality_level`: character varying(20) NULL
- `device_type`: character varying(50) NULL
- `ip_address`: inet NULL
- `device_info`: jsonb NOT NULL
- `updated_at`: timestamp with time zone NULL
- `created_at`: timestamp with time zone NULL

**Foreign Keys:**
- `media_id` -> `media.id`
- `users_id` -> `users.id`

### users_ratings

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `users_id`: integer NOT NULL
- `media_id`: integer NOT NULL
- `user_score`: integer NOT NULL
- `review_text`: text NULL
- `is_public`: boolean NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL

**Foreign Keys:**
- `media_id` -> `media.id`
- `users_id` -> `users.id`

### users_referral_earnings

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `referrer_users_id`: integer NOT NULL
- `referred_users_id`: integer NOT NULL
- `referral_code_id`: integer NULL
- `earning_type`: character varying(30) NOT NULL
- `amount`: numeric(15,2) NOT NULL
- `currency`: character varying(3) NOT NULL
- `credits_awarded`: integer NOT NULL
- `reference_transaction_id`: integer NULL
- `status`: character varying(20) NOT NULL
- `paid_at`: timestamp with time zone NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL

**Foreign Keys:**
- `referral_code_id` -> `referral_codes.id`
- `referred_users_id` -> `users.id`
- `referrer_users_id` -> `users.id`

### users_sessions

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `users_id`: integer NOT NULL
- `session_token`: character varying(255) NOT NULL
- `device_info`: jsonb NOT NULL
- `ip_address`: inet NULL
- `is_active`: boolean NOT NULL
- `last_activity_at`: timestamp with time zone NULL
- `expires_at`: timestamp with time zone NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL

**Foreign Keys:**
- `users_id` -> `users.id`

### users_types

**Primary Key:** id

**Columns:**
- `id`: integer NOT NULL
- `code`: character varying(50) NOT NULL
- `name`: character varying(255) NOT NULL
- `description`: text NULL
- `max_uploads`: integer NOT NULL
- `max_storage_mb`: integer NOT NULL
- `can_resell`: boolean NOT NULL
- `created_at`: timestamp with time zone NULL
- `updated_at`: timestamp with time zone NULL
- `created_by`: integer NULL
- `updated_by`: integer NULL

**Foreign Keys:**
- `created_by` -> `users.id`
- `updated_by` -> `users.id`

