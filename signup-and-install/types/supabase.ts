export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export interface Database {
  public: {
    Tables: {
      accounts: {
        Row: {
          account_name: string | null
          account_status: string | null
          account_uuid: string | null
          clerk_id: string | null
          created_at: string | null
          domain: string | null
          id: number
          install_email: string | null
          monday_access_token: string | null
          monday_account_id: string | null
          monday_account_max_users: number | null
          monday_account_tier: string | null
          monday_chatbots_board_id: number | null
          monday_documents_board_id: number | null
          monday_install_date: string | null
          monday_install_email: string | null
          monday_install_user_id: number | null
          monday_install_user_name: string | null
          monday_training_board_id: number | null
          monday_usage_board_id: number | null
          payment_email: string | null
          slack_install_date: string | null
          slack_install_email: string | null
          slack_team_id: string | null
          subscription_end_date: string | null
          subscription_start_date: string | null
          token: string | null
        }
        Insert: {
          account_name?: string | null
          account_status?: string | null
          account_uuid?: string | null
          clerk_id?: string | null
          created_at?: string | null
          domain?: string | null
          id?: number
          install_email?: string | null
          monday_access_token?: string | null
          monday_account_id?: string | null
          monday_account_max_users?: number | null
          monday_account_tier?: string | null
          monday_chatbots_board_id?: number | null
          monday_documents_board_id?: number | null
          monday_install_date?: string | null
          monday_install_email?: string | null
          monday_install_user_id?: number | null
          monday_install_user_name?: string | null
          monday_training_board_id?: number | null
          monday_usage_board_id?: number | null
          payment_email?: string | null
          slack_install_date?: string | null
          slack_install_email?: string | null
          slack_team_id?: string | null
          subscription_end_date?: string | null
          subscription_start_date?: string | null
          token?: string | null
        }
        Update: {
          account_name?: string | null
          account_status?: string | null
          account_uuid?: string | null
          clerk_id?: string | null
          created_at?: string | null
          domain?: string | null
          id?: number
          install_email?: string | null
          monday_access_token?: string | null
          monday_account_id?: string | null
          monday_account_max_users?: number | null
          monday_account_tier?: string | null
          monday_chatbots_board_id?: number | null
          monday_documents_board_id?: number | null
          monday_install_date?: string | null
          monday_install_email?: string | null
          monday_install_user_id?: number | null
          monday_install_user_name?: string | null
          monday_training_board_id?: number | null
          monday_usage_board_id?: number | null
          payment_email?: string | null
          slack_install_date?: string | null
          slack_install_email?: string | null
          slack_team_id?: string | null
          subscription_end_date?: string | null
          subscription_start_date?: string | null
          token?: string | null
        }
        Relationships: []
      }
      chatbot_trainings: {
        Row: {
          account_id: number | null
          chatbot_id: number | null
          created_at: string | null
          end_time: string | null
          id: number
          monday_account_id: number | null
          monday_board_id: number | null
          monday_item_id: number | null
          name: string | null
          start_time: string | null
          status: string | null
          test_source: string | null
          tokens_used: number | null
        }
        Insert: {
          account_id?: number | null
          chatbot_id?: number | null
          created_at?: string | null
          end_time?: string | null
          id?: number
          monday_account_id?: number | null
          monday_board_id?: number | null
          monday_item_id?: number | null
          name?: string | null
          start_time?: string | null
          status?: string | null
          test_source?: string | null
          tokens_used?: number | null
        }
        Update: {
          account_id?: number | null
          chatbot_id?: number | null
          created_at?: string | null
          end_time?: string | null
          id?: number
          monday_account_id?: number | null
          monday_board_id?: number | null
          monday_item_id?: number | null
          name?: string | null
          start_time?: string | null
          status?: string | null
          test_source?: string | null
          tokens_used?: number | null
        }
        Relationships: [
          {
            foreignKeyName: "chatbot_trainings_account_id_fkey"
            columns: ["account_id"]
            referencedRelation: "accounts"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "chatbot_trainings_account_id_fkey"
            columns: ["account_id"]
            referencedRelation: "decrypted_accounts"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "chatbot_trainings_chatbot_id_fkey"
            columns: ["chatbot_id"]
            referencedRelation: "chatbots"
            referencedColumns: ["id"]
          }
        ]
      }
      chatbots: {
        Row: {
          account_id: number | null
          chatbots_board_id: number | null
          created_at: string | null
          documents_board_id: number | null
          group_internal_name: string | null
          group_name: string | null
          id: number
          index_internal_name: string | null
          item_id: number | null
          name: string | null
          status: string | null
        }
        Insert: {
          account_id?: number | null
          chatbots_board_id?: number | null
          created_at?: string | null
          documents_board_id?: number | null
          group_internal_name?: string | null
          group_name?: string | null
          id?: number
          index_internal_name?: string | null
          item_id?: number | null
          name?: string | null
          status?: string | null
        }
        Update: {
          account_id?: number | null
          chatbots_board_id?: number | null
          created_at?: string | null
          documents_board_id?: number | null
          group_internal_name?: string | null
          group_name?: string | null
          id?: number
          index_internal_name?: string | null
          item_id?: number | null
          name?: string | null
          status?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "chatbots_account_id_fkey"
            columns: ["account_id"]
            referencedRelation: "accounts"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "chatbots_account_id_fkey"
            columns: ["account_id"]
            referencedRelation: "decrypted_accounts"
            referencedColumns: ["id"]
          }
        ]
      }
      documents: {
        Row: {
          archived: boolean | null
          bucket_location: string | null
          chatbot_id: number | null
          creation_date: string | null
          document_description: string | null
          document_name: string | null
          document_object: string | null
          document_type: string | null
          file_name: string | null
          file_status: string | null
          group_name: string | null
          id: number
          item_id: number | null
          monday_account_id: string | null
          private_monday_url: string | null
          public_monday_url: string | null
        }
        Insert: {
          archived?: boolean | null
          bucket_location?: string | null
          chatbot_id?: number | null
          creation_date?: string | null
          document_description?: string | null
          document_name?: string | null
          document_object?: string | null
          document_type?: string | null
          file_name?: string | null
          file_status?: string | null
          group_name?: string | null
          id?: number
          item_id?: number | null
          monday_account_id?: string | null
          private_monday_url?: string | null
          public_monday_url?: string | null
        }
        Update: {
          archived?: boolean | null
          bucket_location?: string | null
          chatbot_id?: number | null
          creation_date?: string | null
          document_description?: string | null
          document_name?: string | null
          document_object?: string | null
          document_type?: string | null
          file_name?: string | null
          file_status?: string | null
          group_name?: string | null
          id?: number
          item_id?: number | null
          monday_account_id?: string | null
          private_monday_url?: string | null
          public_monday_url?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "documents_bucket_location_fkey"
            columns: ["bucket_location"]
            referencedRelation: "buckets"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "documents_chatbot_id_fkey"
            columns: ["chatbot_id"]
            referencedRelation: "chatbots"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "documents_document_object_fkey"
            columns: ["document_object"]
            referencedRelation: "objects"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "documents_monday_account_id_fkey"
            columns: ["monday_account_id"]
            referencedRelation: "accounts"
            referencedColumns: ["monday_account_id"]
          },
          {
            foreignKeyName: "documents_monday_account_id_fkey"
            columns: ["monday_account_id"]
            referencedRelation: "decrypted_accounts"
            referencedColumns: ["monday_account_id"]
          }
        ]
      }
      subscriptions: {
        Row: {
          amount: number | null
          cancelled: boolean | null
          created_at: string | null
          end_date: string | null
          name: string | null
          start_date: string | null
          subscription_id: number
        }
        Insert: {
          amount?: number | null
          cancelled?: boolean | null
          created_at?: string | null
          end_date?: string | null
          name?: string | null
          start_date?: string | null
          subscription_id?: number
        }
        Update: {
          amount?: number | null
          cancelled?: boolean | null
          created_at?: string | null
          end_date?: string | null
          name?: string | null
          start_date?: string | null
          subscription_id?: number
        }
        Relationships: []
      }
      usage: {
        Row: {
          account_id: number | null
          answer: string | null
          created_at: string | null
          id: number
          index_namespace: string | null
          prompt: string | null
          prompter: string | null
          tokens_used: number | null
        }
        Insert: {
          account_id?: number | null
          answer?: string | null
          created_at?: string | null
          id?: number
          index_namespace?: string | null
          prompt?: string | null
          prompter?: string | null
          tokens_used?: number | null
        }
        Update: {
          account_id?: number | null
          answer?: string | null
          created_at?: string | null
          id?: number
          index_namespace?: string | null
          prompt?: string | null
          prompter?: string | null
          tokens_used?: number | null
        }
        Relationships: [
          {
            foreignKeyName: "usage_account_id_fkey"
            columns: ["account_id"]
            referencedRelation: "accounts"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "usage_account_id_fkey"
            columns: ["account_id"]
            referencedRelation: "decrypted_accounts"
            referencedColumns: ["id"]
          }
        ]
      }
      users: {
        Row: {
          account_id: number | null
          created_at: string | null
          email: string | null
          encryption_key: string
          first_name: string | null
          id: number
          last_name: string | null
        }
        Insert: {
          account_id?: number | null
          created_at?: string | null
          email?: string | null
          encryption_key?: string
          first_name?: string | null
          id: number
          last_name?: string | null
        }
        Update: {
          account_id?: number | null
          created_at?: string | null
          email?: string | null
          encryption_key?: string
          first_name?: string | null
          id?: number
          last_name?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "users_account_id_fkey"
            columns: ["account_id"]
            referencedRelation: "accounts"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "users_account_id_fkey"
            columns: ["account_id"]
            referencedRelation: "decrypted_accounts"
            referencedColumns: ["id"]
          }
        ]
      }
    }
    Views: {
      decrypted_accounts: {
        Row: {
          account_name: string | null
          account_status: string | null
          account_uuid: string | null
          clerk_id: string | null
          created_at: string | null
          decrypted_monday_access_token: string | null
          domain: string | null
          id: number | null
          install_email: string | null
          monday_access_token: string | null
          monday_account_id: string | null
          monday_account_max_users: number | null
          monday_account_tier: string | null
          monday_chatbots_board_id: number | null
          monday_documents_board_id: number | null
          monday_install_date: string | null
          monday_install_email: string | null
          monday_install_user_id: number | null
          monday_install_user_name: string | null
          monday_training_board_id: number | null
          monday_usage_board_id: number | null
          payment_email: string | null
          slack_install_date: string | null
          slack_install_email: string | null
          slack_team_id: string | null
          subscription_end_date: string | null
          subscription_start_date: string | null
          token: string | null
        }
        Insert: {
          account_name?: string | null
          account_status?: string | null
          account_uuid?: string | null
          clerk_id?: string | null
          created_at?: string | null
          decrypted_monday_access_token?: never
          domain?: string | null
          id?: number | null
          install_email?: string | null
          monday_access_token?: string | null
          monday_account_id?: string | null
          monday_account_max_users?: number | null
          monday_account_tier?: string | null
          monday_chatbots_board_id?: number | null
          monday_documents_board_id?: number | null
          monday_install_date?: string | null
          monday_install_email?: string | null
          monday_install_user_id?: number | null
          monday_install_user_name?: string | null
          monday_training_board_id?: number | null
          monday_usage_board_id?: number | null
          payment_email?: string | null
          slack_install_date?: string | null
          slack_install_email?: string | null
          slack_team_id?: string | null
          subscription_end_date?: string | null
          subscription_start_date?: string | null
          token?: string | null
        }
        Update: {
          account_name?: string | null
          account_status?: string | null
          account_uuid?: string | null
          clerk_id?: string | null
          created_at?: string | null
          decrypted_monday_access_token?: never
          domain?: string | null
          id?: number | null
          install_email?: string | null
          monday_access_token?: string | null
          monday_account_id?: string | null
          monday_account_max_users?: number | null
          monday_account_tier?: string | null
          monday_chatbots_board_id?: number | null
          monday_documents_board_id?: number | null
          monday_install_date?: string | null
          monday_install_email?: string | null
          monday_install_user_id?: number | null
          monday_install_user_name?: string | null
          monday_training_board_id?: number | null
          monday_usage_board_id?: number | null
          payment_email?: string | null
          slack_install_date?: string | null
          slack_install_email?: string | null
          slack_team_id?: string | null
          subscription_end_date?: string | null
          subscription_start_date?: string | null
          token?: string | null
        }
        Relationships: []
      }
    }
    Functions: {
      decrypt_access_token: {
        Args: {
          p_key: string
          p_encrypted_access_token: string
        }
        Returns: string
      }
      encrypt_access_token: {
        Args: {
          p_key: string
          p_access_token: string
        }
        Returns: string
      }
      generate_uuid: {
        Args: Record<PropertyKey, never>
        Returns: string
      }
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}
