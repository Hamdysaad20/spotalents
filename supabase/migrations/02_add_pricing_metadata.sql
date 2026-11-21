-- ==============================================================================
-- Migration: 02_add_pricing_metadata.sql
-- Description: Adds pricing plan, billing cycle, and compensation metadata columns
-- to public.leads to integrate with the Spotalents admin dashboard and billing sync.
-- ==============================================================================

ALTER TABLE public.leads 
ADD COLUMN IF NOT EXISTS plan VARCHAR(50),
ADD COLUMN IF NOT EXISTS billing VARCHAR(50),
ADD COLUMN IF NOT EXISTS talent_comp VARCHAR(50),
ADD COLUMN IF NOT EXISTS talent_fee VARCHAR(50);

-- Indexes for dashboard filtering by plan and billing cycle
CREATE INDEX IF NOT EXISTS idx_leads_plan ON public.leads (plan);
CREATE INDEX IF NOT EXISTS idx_leads_billing ON public.leads (billing);

COMMENT ON COLUMN public.leads.plan IS 'Selected pricing plan tier: discover, intelligence, enterprise, calibration, general';
COMMENT ON COLUMN public.leads.billing IS 'Billing cycle: annual or monthly';
COMMENT ON COLUMN public.leads.talent_comp IS 'Configured monthly talent compensation if calibrated';
COMMENT ON COLUMN public.leads.talent_fee IS 'Calculated monthly Spotalents engagement fee if calibrated';
