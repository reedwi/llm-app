from dataclasses import dataclass

@dataclass
class TrainingDocQueueMsg:
    monday_account_id: int
    public_monday_url: str
    private_monday_url: str
    document_name: str
    document_type: str
    group_name: str
    file_name: str
    file_status: str
    item_id: int
    asset_id: int
    chatbot_db_id: int
    chatbot_item_id: int
    account_db_id: int
    last_asset: bool
