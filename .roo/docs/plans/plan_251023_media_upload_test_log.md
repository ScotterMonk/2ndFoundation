2025-10-23 19:22; Started testing media upload workflow
2025-10-23 19:25; Verified disabled state (no owner): Media Type dropdown, File input, and Upload button are all correctly disabled
2025-10-23 19:29; Issue identified: Form controls are server-side disabled based on owner variable, not JavaScript controlled. Owner field is readonly, so manual input doesn't enable form.