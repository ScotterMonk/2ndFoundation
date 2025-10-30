# Model Comparison Results

*Generated on: 2025-10-26 12:53:02*

## Summary

- **Tables with discrepancies:** 54
- **Tables only in database:** 3

## Tables Only in Database

- `tv_channels`
- `user_media_affinity`
- `media_backup`

## media_quality_levels


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `is_default` | boolean NOT | Boolean |
| `id` | integer NOT | Integer |
| `resolution_width` | integer | Integer |
| `file_size_bytes` | bigint NOT | BigInteger |
| `bitrate_kbps` | integer | Integer |
| `resolution_height` | integer | Integer |
| `media_id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## files


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `updated_by` | integer | Integer |
| `episode_id` | integer | Integer |
| `media_id` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

### Foreign Keys in Database but Missing from Model

- `created_by` -> `users.id`
- `updated_by` -> `users.id`

## credit_transactions


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `balance_before` | integer NOT | Integer |
| `payment_id` | integer | Integer |
| `id` | integer NOT | Integer |
| `amount` | integer NOT | Integer |
| `balance_after` | integer NOT | Integer |
| `users_id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `updated_by` | integer | Integer |
| `reference_id` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## playlists_media_items


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `added_by` | integer | Integer |
| `sort_order` | integer NOT | Integer |
| `playlist_id` | integer NOT | Integer |
| `media_id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## subscriptions_plans


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `features` | jsonb NOT | JSON |
| `max_storage_mb` | integer | Integer |
| `sort_order` | integer NOT | Integer |
| `duration_days` | integer NOT | Integer |
| `max_uploads` | integer | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `is_active` | boolean NOT | Boolean |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## users_actions

### Columns in Database but Missing from Model

- `created_by`
- `updated_at`
- `updated_by`

### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `target_id` | integer | Integer |
| `users_id` | integer NOT | Integer |
| `action_data` | jsonb NOT | JSON |
| `ip_address` | inet | String |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

### Foreign Keys in Database but Missing from Model

- `created_by` -> `users.id`
- `updated_by` -> `users.id`

## referral_codes


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `usage_limit` | integer NOT | Integer |
| `referrer_users_id` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `reward_value` | integer | Integer |
| `created_by` | integer | Integer |
| `is_active` | boolean NOT | Boolean |
| `current_uses` | integer NOT | Integer |
| `referred_users_id` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## playlists


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `is_public` | boolean NOT | Boolean |
| `updated_by` | integer | Integer |
| `users_id` | integer NOT | Integer |
| `created_by` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## performers


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `tmdb_id` | integer | Integer |
| `gender` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## resellers_settings


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `reseller_id` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |
| `reseller_id` | NULL | nullable=False |
| `setting_type` | NULL | nullable=False |
| `setting_key` | NULL | nullable=False |

## media_performers


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `gender` | integer | Integer |
| `performer_id` | integer NOT | Integer |
| `media_id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

### Foreign Keys in Model but Missing from Database

- `performer_id` -> `performers.id`

## users_referral_earnings


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `referrer_users_id` | integer NOT | Integer |
| `referred_users_id` | integer NOT | Integer |
| `reference_transaction_id` | integer | Integer |
| `credits_awarded` | integer NOT | Integer |
| `referral_code_id` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## users_types


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `max_storage_mb` | integer NOT | Integer |
| `max_uploads` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `can_resell` | boolean NOT | Boolean |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## events


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `events_type_id` | integer NOT | Integer |
| `id` | bigint NOT | BigInteger |
| `event_data` | jsonb NOT | JSON |
| `updated_by` | integer | Integer |
| `users_id` | integer | Integer |
| `created_by` | integer | Integer |
| `ip_address` | inet | String |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## resellers_assets


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `file_size_bytes` | integer | Integer |
| `reseller_id` | integer NOT | Integer |
| `sort_order` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `is_active` | boolean NOT | Boolean |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |
| `reseller_id` | NULL | nullable=False |
| `asset_type` | NULL | nullable=False |
| `sort_order` | NULL | nullable=False |
| `asset_name` | NULL | nullable=False |
| `file_path` | NULL | nullable=False |
| `is_active` | NULL | nullable=False |

## genres


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## support_tickets


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `users_id` | integer NOT | Integer |
| `assigned_to_users_id` | integer | Integer |
| `created_by` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## api_keys


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `users_id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `permissions` | jsonb NOT | JSON |
| `is_active` | boolean NOT | Boolean |
| `rate_limit_per_hour` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## users_sessions

### Columns in Database but Missing from Model

- `updated_at`
- `users_id`
- `is_active`
- `last_activity_at`
- `device_info`

### Columns in Model but Missing from Database

- `user_agent`
- `last_activity`
- `user_id`

### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `ip_address` | inet | String |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

### Foreign Keys in Database but Missing from Model

- `users_id` -> `users.id`

### Foreign Keys in Model but Missing from Database

- `user_id` -> `users.id`

## media_ignore


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `media_id` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## subscriptions_history


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `subscription_id` | integer NOT | Integer |
| `users_id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `subscriptions_plan_id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## users_ratings


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `is_public` | boolean NOT | Boolean |
| `user_score` | integer NOT | Integer |
| `users_id` | integer NOT | Integer |
| `media_id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## resellers_details


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `is_approved` | boolean NOT | Boolean |
| `id` | integer NOT | Integer |
| `users_id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `users_counter` | integer NOT | Integer |
| `payout_details` | jsonb NOT | JSON |
| `users_max` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `total_referrals` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `pending_earnings` | NULL | nullable=False |
| `is_approved` | NULL | nullable=False |
| `id` | NULL | nullable=False |
| `total_earnings` | NULL | nullable=False |
| `users_id` | NULL | nullable=False |
| `paid_earnings` | NULL | nullable=False |
| `users_counter` | NULL | nullable=False |
| `payout_details` | NULL | nullable=False |
| `users_max` | NULL | nullable=False |
| `min_payout_amount` | NULL | nullable=False |
| `commission_rate` | NULL | nullable=False |
| `total_referrals` | NULL | nullable=False |

## media_directors


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `director_id` | integer | Integer |
| `media_id` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## tickets_messages


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `is_internal` | boolean NOT | Boolean |
| `ticket_id` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `message` | text NOT | Text |
| `users_id` | integer NOT | Integer |
| `created_by` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## media_categories


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `sort_order` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `parent_id` | integer | Integer |
| `is_active` | boolean NOT | Boolean |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## media


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `runtime` | integer | Integer |
| `total_seasons` | integer | Integer |
| `file_size_bytes` | bigint NOT | BigInteger |
| `vote_count` | integer | Integer |
| `filename_original` | character varying NOT | String |
| `is_processed` | boolean NOT | Boolean |
| `other_id` | integer | Integer |
| `view_count` | integer NOT | Integer |
| `id` | integer NOT | Integer |
| `is_public` | boolean NOT | Boolean |
| `is_featured` | boolean NOT | Boolean |
| `users_id` | integer NOT | Integer |
| `download_count` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `video_trailer_file_id` | integer | Integer |
| `mime_type` | character varying NOT | String |
| `media_type_id` | integer NOT | Integer |
| `metadata` | jsonb NOT | JSON |
| `adult` | boolean NOT | Boolean |
| `like_count` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `title` | character varying NOT | String |
| `content_id` | integer | Integer |
| `filename_stored` | character varying NOT | String |
| `tvdb_id` | integer | Integer |
| `file_path` | character varying NOT | String |
| `min_age` | integer NOT | Integer |
| `tmdb_id` | integer | Integer |
| `total_episodes` | integer | Integer |
| `processing_status` | character varying NOT | String |
| `credit_cost` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## users_faves_performers


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `user_id` | integer | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `weight` | integer | Integer |
| `performer_id` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## directors


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `updated_by` | integer | Integer |
| `tmdb_id` | integer | Integer |
| `gender` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## content_reports


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `reported_by_users_id` | integer | Integer |
| `id` | integer NOT | Integer |
| `description` | text NOT | Text |
| `resolved_by_users_id` | integer | Integer |
| `media_id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## users_devices

### Columns in Database but Missing from Model

- `last_used_at`
- `updated_at`
- `browser_info`
- `location_info`
- `users_id`
- `ip_address`

### Columns in Model but Missing from Database

- `last_active`
- `is_blocked`
- `user_id`
- `login_count`

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

## episodes


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `vote_count` | integer | Integer |
| `episode_number` | integer | Integer |
| `updated_by` | integer | Integer |
| `season_number` | integer | Integer |
| `created_by` | integer | Integer |
| `media_id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

### Foreign Keys in Database but Missing from Model

- `created_by` -> `users.id`
- `updated_by` -> `users.id`

## users_faves_genres


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `genre_id` | integer NOT | Integer |
| `id` | integer NOT | Integer |
| `user_id` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `weight` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## events_types


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `is_tracked` | boolean NOT | Boolean |
| `id` | integer NOT | Integer |
| `retention_days` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## invitations


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `inviter_users_id` | integer NOT | Integer |
| `id` | integer NOT | Integer |
| `accepted_users_id` | integer | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## media_subtitles


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `is_default` | boolean NOT | Boolean |
| `id` | integer NOT | Integer |
| `file_size_bytes` | integer | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `media_id` | integer NOT | Integer |
| `language_id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

### Foreign Keys in Database but Missing from Model

- `created_by` -> `users.id`
- `updated_by` -> `users.id`

## payments


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `subscription_id` | integer | Integer |
| `credit_package_id` | integer | Integer |
| `updated_by` | integer | Integer |
| `users_id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `gateway_response` | jsonb NOT | JSON |
| `credits_purchased` | integer | Integer |
| `payment_method_id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## media_categories_assignments


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `category_id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `media_id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

### Foreign Keys in Database but Missing from Model

- `created_by` -> `users.id`

## transactions


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `receiver_users_id` | integer | Integer |
| `transactions_type_id` | integer NOT | Integer |
| `sender_users_id` | integer | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `payment_method_id` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## system_settings


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

### Foreign Keys in Model but Missing from Database

- `created_by` -> `users.id`
- `updated_by` -> `users.id`

## payment_methods


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `is_active` | boolean NOT | Boolean |
| `configuration` | jsonb NOT | JSON |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## resellers_commissions


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `customer_users_id` | integer NOT | Integer |
| `reference_id` | integer | Integer |
| `reseller_users_id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `status` | NULL | nullable=False |
| `id` | NULL | nullable=False |
| `base_amount` | NULL | nullable=False |
| `commission_amount` | NULL | nullable=False |
| `commission_rate` | NULL | nullable=False |
| `customer_users_id` | NULL | nullable=False |
| `currency` | NULL | nullable=False |
| `transaction_type` | NULL | nullable=False |
| `reseller_users_id` | NULL | nullable=False |

## notifications

### Columns in Database but Missing from Model

- `updated_at`
- `metadata`
- `users_id`
- `created_by`
- `expires_at`
- `is_sent`

### Columns in Model but Missing from Database

- `action_data`
- `read_at`
- `user_id`

### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `is_read` | boolean NOT | Boolean |
| `message` | text NOT | Text |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

### Foreign Keys in Database but Missing from Model

- `created_by` -> `users.id`
- `users_id` -> `users.id`

### Foreign Keys in Model but Missing from Database

- `user_id` -> `users.id`

## media_types


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `allowed_extensions` | _text[] | ARRAY |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `max_file_size_mb` | integer | Integer |
| `requires_processing` | boolean NOT | Boolean |
| `credit_cost` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## subscriptions


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `auto_renew` | boolean NOT | Boolean |
| `updated_by` | integer | Integer |
| `users_id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `subscriptions_plan_id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## users


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `is_locked_out` | boolean NOT | Boolean |
| `total_storage_used_mb` | integer NOT | Integer |
| `payee_id` | integer | Integer |
| `new_episode_notification` | boolean NOT | Boolean |
| `is_active` | boolean NOT | Boolean |
| `failed_login_attempts` | integer NOT | Integer |
| `is_verified` | boolean NOT | Boolean |
| `id` | integer NOT | Integer |
| `preferences` | jsonb NOT | JSON |
| `created_by` | integer | Integer |
| `notification_settings` | jsonb NOT | JSON |
| `referred_by_users_id` | integer | Integer |
| `is_verified_phone` | boolean NOT | Boolean |
| `is_verified_email` | boolean NOT | Boolean |
| `updated_by` | integer | Integer |
| `parent_id` | integer | Integer |
| `users_type_id` | integer NOT | Integer |
| `credit_balance` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## languages


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `is_active` | boolean NOT | Boolean |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## users_faves_directors


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `user_id` | integer | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `weight` | integer | Integer |
| `director_id` | integer | Integer |

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

## users_media_affinity


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | bigint NOT | BigInteger |
| `affinity_metadata` | jsonb NOT | JSON |
| `users_id` | integer NOT | Integer |
| `affinity_score` | real NOT | Float |
| `media_id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## users_media_history


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `credits_spent` | integer NOT | Integer |
| `id` | bigint NOT | BigInteger |
| `media_id` | integer NOT | Integer |
| `completion_percentage` | integer NOT | Integer |
| `users_id` | integer NOT | Integer |
| `ip_address` | inet | String |
| `playback_position_seconds` | integer NOT | Integer |
| `device_info` | jsonb NOT | JSON |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## transactions_types


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## media_genres


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `genre_id` | integer NOT | Integer |
| `id` | integer NOT | Integer |
| `created_by` | integer | Integer |
| `media_id` | integer NOT | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

### Foreign Keys in Database but Missing from Model

- `created_by` -> `users.id`

## users_favorites


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `id` | integer NOT | Integer |
| `users_id` | integer | Integer |
| `media_id` | integer | Integer |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |

## credit_packages


### Type Mismatches

| Column | Database Type | Model Type |
|--------|--------------|------------|
| `credit_amount` | integer NOT | Integer |
| `id` | integer NOT | Integer |
| `bonus_credits` | integer NOT | Integer |
| `sort_order` | integer NOT | Integer |
| `updated_by` | integer | Integer |
| `created_by` | integer | Integer |
| `is_active` | boolean NOT | Boolean |

### Nullability Mismatches

| Column | Database | Model |
|--------|----------|-------|
| `id` | NULL | nullable=False |
