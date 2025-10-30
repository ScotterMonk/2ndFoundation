# Model Comparison Results

*Generated on: 2025-10-26 12:42:54*

## Summary

- **Tables with discrepancies:** 54
- **Tables only in database:** 3

## Tables Only in Database

- `user_media_affinity`
- `media_backup`
- `tv_channels`

## languages


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `is_active` | boolean NOT | Boolean |
| `id` | integer NOT | Integer |
| `created_by` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## tickets_messages


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `ticket_id` | integer NOT | Integer |
| `is_internal` | boolean NOT | Boolean |
| `users_id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `message` | text NOT | Text |
| `id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## users_media_affinity


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `affinity_metadata` | jsonb NOT | JSON |
| `id` | bigint NOT | BigInteger |
| `users_id` | integer NOT | Integer |
| `affinity_score` | real NOT | Float |
| `media_id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## users_faves_directors


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `director_id` | integer | Integer |
| `weight` | integer | Integer |
| `user_id` | integer | Integer |
| `created_by` | integer | Integer |
| `id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

### Primary Key Mismatch

- **Database:** 
- **Model:** `id`

### Foreign Keys in Model but Missing from Database

- `created_by` -> `users.id`
- `updated_by` -> `users.id`

## subscriptions_history


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `subscriptions_plan_id` | integer NOT | Integer |
| `users_id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `subscription_id` | integer NOT | Integer |
| `id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## users


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `is_locked_out` | boolean NOT | Boolean |
| `new_episode_notification` | boolean NOT | Boolean |
| `created_by` | integer | Integer |
| `parent_id` | integer | Integer |
| `credit_balance` | integer NOT | Integer |
| `preferences` | jsonb NOT | JSON |
| `failed_login_attempts` | integer NOT | Integer |
| `payee_id` | integer | Integer |
| `updated_by` | integer | Integer |
| `is_verified_email` | boolean NOT | Boolean |
| `id` | integer NOT | Integer |
| `referred_by_users_id` | integer | Integer |
| `total_storage_used_mb` | integer NOT | Integer |
| `users_type_id` | integer NOT | Integer |
| `is_verified_phone` | boolean NOT | Boolean |
| `is_active` | boolean NOT | Boolean |
| `is_verified` | boolean NOT | Boolean |
| `notification_settings` | jsonb NOT | JSON |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## payment_methods


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `is_active` | boolean NOT | Boolean |
| `id` | integer NOT | Integer |
| `configuration` | jsonb NOT | JSON |
| `created_by` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## subscriptions_plans


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `max_storage_mb` | integer | Integer |
| `duration_days` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `is_active` | boolean NOT | Boolean |
| `sort_order` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `max_uploads` | integer | Integer |
| `features` | jsonb NOT | JSON |
| `id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## directors


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `gender` | integer | Integer |
| `tmdb_id` | integer | Integer |
| `created_by` | integer | Integer |
| `id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## media_subtitles


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `is_default` | boolean NOT | Boolean |
| `file_size_bytes` | integer | Integer |
| `created_by` | integer | Integer |
| `language_id` | integer NOT | Integer |
| `id` | integer NOT | Integer |
| `media_id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

### Foreign Keys in Database but Missing from Model

- `created_by` -> `users.id`
- `updated_by` -> `users.id`

## credit_packages


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `is_active` | boolean NOT | Boolean |
| `sort_order` | integer NOT | Integer |
| `bonus_credits` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `id` | integer NOT | Integer |
| `credit_amount` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## resellers_assets


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `reseller_id` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `is_active` | boolean NOT | Boolean |
| `sort_order` | integer NOT | Integer |
| `file_size_bytes` | integer | Integer |
| `created_by` | integer | Integer |
| `id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `reseller_id` | NULL | nullable=False |
| `is_active` | NULL | nullable=False |
| `sort_order` | NULL | nullable=False |
| `asset_name` | NULL | nullable=False |
| `file_path` | NULL | nullable=False |
| `asset_type` | NULL | nullable=False |
| `id` | NULL | nullable=False |

## episodes


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `season_number` | integer | Integer |
| `episode_number` | integer | Integer |
| `vote_count` | integer | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `id` | integer NOT | Integer |
| `media_id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

### Foreign Keys in Database but Missing from Model

- `created_by` -> `users.id`
- `updated_by` -> `users.id`

## media_performers


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `gender` | integer | Integer |
| `performer_id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `id` | integer NOT | Integer |
| `media_id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

### Foreign Keys in Model but Missing from Database

- `performer_id` -> `performers.id`

## genres


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## users_sessions

### Columns in Database but Missing from Model

- `updated_at`
- `is_active`
- `users_id`
- `last_activity_at`
- `device_info`

### Columns in Model but Missing from Database

- `user_agent`
- `last_activity`
- `user_id`

### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `ip_address` | inet | String |
| `id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

### Foreign Keys in Database but Missing from Model

- `users_id` -> `users.id`

### Foreign Keys in Model but Missing from Database

- `user_id` -> `users.id`

## api_keys


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `is_active` | boolean NOT | Boolean |
| `permissions` | jsonb NOT | JSON |
| `users_id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `rate_limit_per_hour` | integer NOT | Integer |
| `id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## resellers_commissions


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `customer_users_id` | integer NOT | Integer |
| `id` | integer NOT | Integer |
| `reseller_users_id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `reference_id` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `commission_rate` | NULL | nullable=False |
| `customer_users_id` | NULL | nullable=False |
| `id` | NULL | nullable=False |
| `reseller_users_id` | NULL | nullable=False |
| `base_amount` | NULL | nullable=False |
| `currency` | NULL | nullable=False |
| `commission_amount` | NULL | nullable=False |
| `status` | NULL | nullable=False |
| `transaction_type` | NULL | nullable=False |

## users_referral_earnings


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `referrer_users_id` | integer NOT | Integer |
| `reference_transaction_id` | integer | Integer |
| `referred_users_id` | integer NOT | Integer |
| `credits_awarded` | integer NOT | Integer |
| `referral_code_id` | integer | Integer |
| `id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## users_actions

### Columns in Database but Missing from Model

- `updated_at`
- `created_by`
- `updated_by`

### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `ip_address` | inet | String |
| `users_id` | integer NOT | Integer |
| `action_data` | jsonb NOT | JSON |
| `target_id` | integer | Integer |
| `id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

### Foreign Keys in Database but Missing from Model

- `created_by` -> `users.id`
- `updated_by` -> `users.id`

## media


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `content_id` | integer | Integer |
| `credit_cost` | integer NOT | Integer |
| `video_trailer_file_id` | integer | Integer |
| `metadata` | jsonb NOT | JSON |
| `mime_type` | character varying NOT | String |
| `filename_original` | character varying NOT | String |
| `created_by` | integer | Integer |
| `min_age` | integer NOT | Integer |
| `filename_stored` | character varying NOT | String |
| `total_seasons` | integer | Integer |
| `tvdb_id` | integer | Integer |
| `users_id` | integer NOT | Integer |
| `file_path` | character varying NOT | String |
| `is_public` | boolean NOT | Boolean |
| `other_id` | integer | Integer |
| `total_episodes` | integer | Integer |
| `title` | character varying NOT | String |
| `vote_count` | integer | Integer |
| `updated_by` | integer | Integer |
| `is_processed` | boolean NOT | Boolean |
| `processing_status` | character varying NOT | String |
| `media_type_id` | integer NOT | Integer |
| `file_size_bytes` | bigint NOT | BigInteger |
| `tmdb_id` | integer | Integer |
| `download_count` | integer NOT | Integer |
| `runtime` | integer | Integer |
| `id` | integer NOT | Integer |
| `view_count` | integer NOT | Integer |
| `like_count` | integer NOT | Integer |
| `is_featured` | boolean NOT | Boolean |
| `adult` | boolean NOT | Boolean |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## system_settings


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

### Foreign Keys in Model but Missing from Database

- `created_by` -> `users.id`
- `updated_by` -> `users.id`

## performers


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `gender` | integer | Integer |
| `tmdb_id` | integer | Integer |
| `created_by` | integer | Integer |
| `id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## users_media_history


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `credits_spent` | integer NOT | Integer |
| `playback_position_seconds` | integer NOT | Integer |
| `ip_address` | inet | String |
| `id` | bigint NOT | BigInteger |
| `users_id` | integer NOT | Integer |
| `completion_percentage` | integer NOT | Integer |
| `media_id` | integer NOT | Integer |
| `device_info` | jsonb NOT | JSON |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## events


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `event_data` | jsonb NOT | JSON |
| `updated_by` | integer | Integer |
| `ip_address` | inet | String |
| `users_id` | integer | Integer |
| `events_type_id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `id` | bigint NOT | BigInteger |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## users_types


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `can_resell` | boolean NOT | Boolean |
| `updated_by` | integer | Integer |
| `id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `max_uploads` | integer NOT | Integer |
| `max_storage_mb` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## media_ignore


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `id` | integer NOT | Integer |
| `media_id` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## media_types


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `credit_cost` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `max_file_size_mb` | integer | Integer |
| `id` | integer NOT | Integer |
| `requires_processing` | boolean NOT | Boolean |
| `allowed_extensions` | _text[] | ARRAY |
| `created_by` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## notifications

### Columns in Database but Missing from Model

- `updated_at`
- `metadata`
- `users_id`
- `created_by`
- `is_sent`
- `expires_at`

### Columns in Model but Missing from Database

- `read_at`
- `action_data`
- `user_id`

### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `is_read` | boolean NOT | Boolean |
| `message` | text NOT | Text |
| `id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

### Foreign Keys in Database but Missing from Model

- `created_by` -> `users.id`
- `users_id` -> `users.id`

### Foreign Keys in Model but Missing from Database

- `user_id` -> `users.id`

## users_faves_performers


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `weight` | integer | Integer |
| `user_id` | integer | Integer |
| `performer_id` | integer | Integer |
| `created_by` | integer | Integer |
| `id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## transactions


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `receiver_users_id` | integer | Integer |
| `id` | integer NOT | Integer |
| `payment_method_id` | integer | Integer |
| `transactions_type_id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `sender_users_id` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## playlists


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `users_id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `is_public` | boolean NOT | Boolean |
| `id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## resellers_settings


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `reseller_id` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `reseller_id` | NULL | nullable=False |
| `setting_type` | NULL | nullable=False |
| `id` | NULL | nullable=False |
| `setting_key` | NULL | nullable=False |

## support_tickets


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `users_id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `assigned_to_users_id` | integer | Integer |
| `id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## invitations


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `inviter_users_id` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `accepted_users_id` | integer | Integer |
| `created_by` | integer | Integer |
| `id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## payments


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `credits_purchased` | integer | Integer |
| `id` | integer NOT | Integer |
| `payment_method_id` | integer NOT | Integer |
| `users_id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `credit_package_id` | integer | Integer |
| `subscription_id` | integer | Integer |
| `gateway_response` | jsonb NOT | JSON |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## media_quality_levels


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `is_default` | boolean NOT | Boolean |
| `resolution_height` | integer | Integer |
| `file_size_bytes` | bigint NOT | BigInteger |
| `resolution_width` | integer | Integer |
| `bitrate_kbps` | integer | Integer |
| `id` | integer NOT | Integer |
| `media_id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## users_favorites


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `users_id` | integer | Integer |
| `id` | integer NOT | Integer |
| `media_id` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## events_types


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `retention_days` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `id` | integer NOT | Integer |
| `is_tracked` | boolean NOT | Boolean |
| `created_by` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## media_categories


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `is_active` | boolean NOT | Boolean |
| `sort_order` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `id` | integer NOT | Integer |
| `parent_id` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## referral_codes


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `is_active` | boolean NOT | Boolean |
| `usage_limit` | integer NOT | Integer |
| `referrer_users_id` | integer NOT | Integer |
| `id` | integer NOT | Integer |
| `reward_value` | integer | Integer |
| `referred_users_id` | integer | Integer |
| `created_by` | integer | Integer |
| `current_uses` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## users_ratings


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `user_score` | integer NOT | Integer |
| `users_id` | integer NOT | Integer |
| `is_public` | boolean NOT | Boolean |
| `id` | integer NOT | Integer |
| `media_id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## playlists_media_items


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `playlist_id` | integer NOT | Integer |
| `sort_order` | integer NOT | Integer |
| `added_by` | integer | Integer |
| `id` | integer NOT | Integer |
| `media_id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## credit_transactions


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `amount` | integer NOT | Integer |
| `id` | integer NOT | Integer |
| `payment_id` | integer | Integer |
| `balance_before` | integer NOT | Integer |
| `users_id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `reference_id` | integer | Integer |
| `balance_after` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## users_faves_genres


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `genre_id` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `weight` | integer | Integer |
| `user_id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## files


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `episode_id` | integer | Integer |
| `id` | integer NOT | Integer |
| `media_id` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

### Foreign Keys in Database but Missing from Model

- `created_by` -> `users.id`
- `updated_by` -> `users.id`

## resellers_details


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `created_by` | integer | Integer |
| `total_referrals` | integer NOT | Integer |
| `users_id` | integer NOT | Integer |
| `users_max` | integer NOT | Integer |
| `payout_details` | jsonb NOT | JSON |
| `users_counter` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `id` | integer NOT | Integer |
| `is_approved` | boolean NOT | Boolean |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `paid_earnings` | NULL | nullable=False |
| `total_referrals` | NULL | nullable=False |
| `users_id` | NULL | nullable=False |
| `users_max` | NULL | nullable=False |
| `payout_details` | NULL | nullable=False |
| `users_counter` | NULL | nullable=False |
| `commission_rate` | NULL | nullable=False |
| `total_earnings` | NULL | nullable=False |
| `id` | NULL | nullable=False |
| `is_approved` | NULL | nullable=False |
| `pending_earnings` | NULL | nullable=False |
| `min_payout_amount` | NULL | nullable=False |

## media_directors


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `director_id` | integer | Integer |
| `created_by` | integer | Integer |
| `id` | integer NOT | Integer |
| `media_id` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## media_categories_assignments


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `category_id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `id` | integer NOT | Integer |
| `media_id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

### Foreign Keys in Database but Missing from Model

- `created_by` -> `users.id`

## media_genres


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `genre_id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `id` | integer NOT | Integer |
| `media_id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

### Foreign Keys in Database but Missing from Model

- `created_by` -> `users.id`

## transactions_types


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `id` | integer NOT | Integer |
| `created_by` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## users_devices

### Columns in Database but Missing from Model

- `updated_at`
- `ip_address`
- `users_id`
- `last_used_at`
- `location_info`
- `browser_info`

### Columns in Model but Missing from Database

- `login_count`
- `last_active`
- `is_blocked`
- `user_id`

### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `is_trusted` | boolean NOT | Boolean |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

### Foreign Keys in Database but Missing from Model

- `users_id` -> `users.id`

### Foreign Keys in Model but Missing from Database

- `user_id` -> `users.id`

## subscriptions


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `updated_by` | integer | Integer |
| `subscriptions_plan_id` | integer NOT | Integer |
| `users_id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `auto_renew` | boolean NOT | Boolean |
| `id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## content_reports


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `resolved_by_users_id` | integer | Integer |
| `media_id` | integer NOT | Integer |
| `description` | text NOT | Text |
| `id` | integer NOT | Integer |
| `reported_by_users_id` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |
