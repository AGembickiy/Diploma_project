export interface Newsletter {
  id: number;
  title: string;
  content: string;
  subject: string;
  status: 'draft' | 'sending' | 'sent' | 'cancelled';
  status_display: string;
  send_to_all: boolean;
  send_to_active: boolean;
  send_to_new: boolean;
  created_by: {
    id: number;
    username: string;
    email: string;
  };
  created_at: string;
  scheduled_at: string | null;
  sent_at: string | null;
  total_recipients: number;
  sent_count: number;
  failed_count: number;
  recipients_count: number;
}

export interface NewsletterCreate {
  title: string;
  content: string;
  subject: string;
  send_to_all: boolean;
  send_to_active: boolean;
  send_to_new: boolean;
  scheduled_at?: string;
}

export interface NewsletterTemplate {
  id: number;
  name: string;
  subject: string;
  content: string;
  is_active: boolean;
  created_at: string;
}

export interface NewsletterRecipient {
  id: number;
  user: {
    id: number;
    username: string;
    email: string;
  };
  status: 'pending' | 'sent' | 'failed' | 'bounced';
  status_display: string;
  sent_at: string | null;
  error_message: string;
}

export interface NewsletterStats {
  total_newsletters: number;
  draft_count: number;
  sending_count: number;
  sent_count: number;
  cancelled_count: number;
  total_recipients: number;
  total_sent: number;
  total_failed: number;
  success_rate: number;
}

export interface NewsletterPreview {
  subject: string;
  content: string;
  recipients_count: number;
  recipients_preview: string[];
}

export interface NewsletterResponse {
  message: string;
  sent_count?: number;
  deleted_count?: number;
}
