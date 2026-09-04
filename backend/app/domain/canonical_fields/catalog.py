"""MVP canonical field catalog.

Codes are a public, stable contract for future method requirements. Rename only
through an explicit data migration and compatibility policy.
"""
from typing import TypedDict


class CanonicalDefinition(TypedDict):
    code: str
    domain: str
    name: str
    description: str
    expected_data_type: str
    expected_grain: str
    unit_type: str
    entity_type: str
    aliases: list[str]


def field(code: str, domain: str, name: str, description: str, data_type: str, grain: str, unit: str, entity: str, *aliases: str) -> CanonicalDefinition:
    return {"code": code, "domain": domain, "name": name, "description": description, "expected_data_type": data_type, "expected_grain": grain, "unit_type": unit, "entity_type": entity, "aliases": list(aliases)}


CANONICAL_FIELDS: list[CanonicalDefinition] = [
    field("ORDER_ID", "SALES", "Order ID", "Stable identifier for an order or invoice.", "text", "ORDER", "IDENTIFIER", "ORDER", "order_id", "invoice_id", "transaction_id", "order_number", "invoice_number"),
    field("ORDER_LINE_ID", "SALES", "Order line ID", "Stable identifier for a line within an order.", "text", "ORDER_LINE", "IDENTIFIER", "ORDER_LINE", "line_id", "order_line_id", "invoice_line_id"),
    field("ORDER_DATE", "SALES", "Order date", "Date an order or invoice was created or issued.", "date", "ORDER", "DATE", "ORDER", "order_date", "invoice_date", "transaction_date", "sale_date", "issue_date"),
    field("ORDER_STATUS", "SALES", "Order status", "Operational status of an order or invoice.", "categorical", "ORDER", "CATEGORY", "ORDER", "order_status", "invoice_status", "sale_status", "status"),
    field("PRODUCT_ID", "SALES", "Product ID", "Stable identifier for a product, service, or SKU.", "text", "PRODUCT", "IDENTIFIER", "PRODUCT", "product_id", "sku", "item_id", "service_id"),
    field("PRODUCT_NAME", "SALES", "Product name", "Human-readable product or service name.", "text", "PRODUCT", "TEXT", "PRODUCT", "product", "product_name", "item", "item_name", "service_name"),
    field("PRODUCT_CATEGORY", "SALES", "Product category", "Grouping assigned to a product or service.", "categorical", "PRODUCT", "CATEGORY", "PRODUCT", "category", "product_category", "item_category", "service_category"),
    field("QUANTITY", "SALES", "Quantity", "Number of units on an order line.", "decimal", "ORDER_LINE", "QUANTITY", "ORDER_LINE", "quantity", "qty", "units", "units_sold"),
    field("UNIT_PRICE", "SALES", "Unit price", "Price charged per unit before or after adjustments according to the source definition; currency must be identified separately.", "decimal", "ORDER_LINE", "CURRENCY", "ORDER_LINE", "unit_price", "price_per_unit", "selling_price", "price"),
    field("UNIT_COST", "SALES", "Unit cost", "Direct cost per unit under the source costing policy; currency must be identified separately.", "decimal", "ORDER_LINE", "CURRENCY", "ORDER_LINE", "unit_cost", "cost_per_unit", "item_cost"),
    field("DISCOUNT_AMOUNT", "SALES", "Discount amount", "Absolute monetary reduction from gross consideration; currency is unknown unless supplied.", "decimal", "ORDER_LINE", "CURRENCY", "ORDER_LINE", "discount_amount", "discount_value"),
    field("DISCOUNT_RATE", "SALES", "Discount rate", "Discount expressed as a fraction or percentage, not a currency amount.", "decimal", "ORDER_LINE", "PERCENTAGE", "ORDER_LINE", "discount_rate", "discount_pct", "discount_percent", "discount"),
    field("GROSS_REVENUE", "SALES", "Gross revenue", "Revenue before discounts, returns, refunds, or allowances. Do not map generic sales values when deductions are unclear.", "decimal", "ORDER_LINE", "CURRENCY", "ORDER_LINE", "gross_revenue", "gross_sales", "gross_amount"),
    field("NET_REVENUE", "SALES", "Net revenue", "Revenue after represented discounts, returns, refunds, or allowances. A generic sales amount requires review of its accounting definition.", "decimal", "ORDER_LINE", "CURRENCY", "ORDER_LINE", "net_revenue", "net_sales", "sales_amount", "invoice_total", "transaction_value", "revenue"),
    field("REGION", "SALES", "Region", "Geographic reporting category associated with a transaction or entity.", "categorical", "UNKNOWN", "CATEGORY", "GEOGRAPHY", "region", "sales_region", "territory", "geography"),
    field("CUSTOMER_ID", "CUSTOMERS", "Customer ID", "Stable identifier under the business's declared person, account, or household identity policy.", "text", "CUSTOMER", "IDENTIFIER", "CUSTOMER", "customer_id", "cust_id", "client_id", "buyer_id", "customer_number", "account_id"),
    field("CUSTOMER_NAME", "CUSTOMERS", "Customer name", "Human-readable customer or account name.", "text", "CUSTOMER", "TEXT", "CUSTOMER", "customer_name", "client_name", "account_name", "buyer_name"),
    field("CUSTOMER_SEGMENT", "CUSTOMERS", "Customer segment", "Business-defined customer grouping.", "categorical", "CUSTOMER", "CATEGORY", "CUSTOMER", "customer_segment", "segment", "customer_type"),
    field("CUSTOMER_CREATED_DATE", "CUSTOMERS", "Customer created date", "Date the customer record or relationship began.", "date", "CUSTOMER", "DATE", "CUSTOMER", "customer_created_date", "signup_date", "registration_date", "acquired_date"),
    field("CUSTOMER_STATUS", "CUSTOMERS", "Customer status", "Current business-defined customer lifecycle status.", "categorical", "CUSTOMER", "CATEGORY", "CUSTOMER", "customer_status", "account_status"),
    field("CAMPAIGN_ID", "MARKETING", "Campaign ID", "Stable identifier for a marketing campaign.", "text", "CAMPAIGN", "IDENTIFIER", "CAMPAIGN", "campaign_id", "campaign_code"),
    field("CAMPAIGN_NAME", "MARKETING", "Campaign name", "Human-readable marketing campaign name.", "text", "CAMPAIGN", "TEXT", "CAMPAIGN", "campaign_name", "campaign"),
    field("MARKETING_CHANNEL", "MARKETING", "Marketing channel", "Channel through which marketing activity occurred.", "categorical", "CAMPAIGN", "CATEGORY", "CAMPAIGN", "marketing_channel", "channel", "source_medium"),
    field("MARKETING_SPEND", "MARKETING", "Marketing spend", "Marketing cost for the represented scope and period; currency must be supplied separately.", "decimal", "CAMPAIGN", "CURRENCY", "CAMPAIGN", "marketing_spend", "ad_spend", "advertising_cost", "campaign_cost", "media_spend"),
    field("IMPRESSIONS", "MARKETING", "Impressions", "Count of delivered or recorded advertising impressions.", "integer", "CAMPAIGN", "COUNT", "CAMPAIGN", "impressions", "impression_count", "views"),
    field("CLICKS", "MARKETING", "Clicks", "Count of recorded marketing clicks.", "integer", "CAMPAIGN", "COUNT", "CAMPAIGN", "clicks", "click_count"),
    field("LEAD_ID", "MARKETING", "Lead ID", "Stable identifier for a prospect or lead.", "text", "UNKNOWN", "IDENTIFIER", "LEAD", "lead_id", "prospect_id"),
    field("CONVERSION_COUNT", "MARKETING", "Conversion count", "Count of conversions under the source's declared conversion definition.", "integer", "CAMPAIGN", "COUNT", "CAMPAIGN", "conversions", "conversion_count", "orders_attributed"),
    field("ACCOUNT_ID", "ACCOUNTING", "Account ID", "Stable chart-of-accounts identifier.", "text", "ACCOUNT", "IDENTIFIER", "ACCOUNT", "account_id", "account_code", "gl_account"),
    field("ACCOUNT_CLASS", "ACCOUNTING", "Account class", "Accounting class such as asset, liability, equity, revenue, expense, gain, or loss.", "categorical", "ACCOUNT", "CATEGORY", "ACCOUNT", "account_class", "account_type", "gl_class"),
    field("JOURNAL_ENTRY_ID", "ACCOUNTING", "Journal entry ID", "Stable identifier for a posted or draft journal entry.", "text", "ACCOUNT", "IDENTIFIER", "JOURNAL_ENTRY", "journal_entry_id", "entry_id", "journal_id"),
    field("POSTING_DATE", "ACCOUNTING", "Posting date", "Accounting date on which a journal entry or balance movement is posted.", "date", "ACCOUNT", "DATE", "JOURNAL_ENTRY", "posting_date", "journal_date", "gl_date"),
    field("DEBIT_AMOUNT", "ACCOUNTING", "Debit amount", "Debit-side amount at journal-line grain; currency must be supplied separately.", "decimal", "ACCOUNT", "CURRENCY", "JOURNAL_LINE", "debit", "debit_amount"),
    field("CREDIT_AMOUNT", "ACCOUNTING", "Credit amount", "Credit-side amount at journal-line grain; currency must be supplied separately.", "decimal", "ACCOUNT", "CURRENCY", "JOURNAL_LINE", "credit", "credit_amount"),
    field("COGS", "FINANCE", "Cost of goods sold", "Direct costs recognized against revenue under the selected accounting policy.", "decimal", "MONTH", "CURRENCY", "BUSINESS", "cogs", "cost_of_goods_sold", "cost_of_sales", "direct_costs"),
    field("GROSS_PROFIT", "FINANCE", "Gross profit", "Net revenue less cost of goods sold for the same scope and period.", "decimal", "MONTH", "CURRENCY", "BUSINESS", "gross_profit"),
    field("OPERATING_EXPENSE", "FINANCE", "Operating expense", "Operating expenses excluding COGS under the source classification policy.", "decimal", "MONTH", "CURRENCY", "BUSINESS", "operating_expense", "opex", "operating_costs"),
    field("CASH", "FINANCE", "Cash", "Cash and cash equivalents under the represented account and restriction policy.", "decimal", "MONTH", "CURRENCY", "BUSINESS", "cash", "cash_balance", "cash_and_equivalents"),
    field("ACCOUNTS_RECEIVABLE", "FINANCE", "Accounts receivable", "Outstanding valid customer receivables at a reporting cutoff.", "decimal", "MONTH", "CURRENCY", "BUSINESS", "accounts_receivable", "ar_balance", "receivables"),
    field("ACCOUNTS_PAYABLE", "FINANCE", "Accounts payable", "Outstanding valid vendor payables at a reporting cutoff.", "decimal", "MONTH", "CURRENCY", "BUSINESS", "accounts_payable", "ap_balance", "payables"),
    field("INVENTORY_QUANTITY", "OPERATIONS", "Inventory quantity", "On-hand inventory units at a location and snapshot date.", "decimal", "INVENTORY_SNAPSHOT", "QUANTITY", "INVENTORY", "inventory_quantity", "quantity_on_hand", "on_hand", "stock_qty"),
    field("INVENTORY_VALUE", "OPERATIONS", "Inventory value", "Inventory carrying value under the selected costing policy; currency must be supplied separately.", "decimal", "INVENTORY_SNAPSHOT", "CURRENCY", "INVENTORY", "inventory_value", "stock_value"),
    field("JOB_ID", "OPERATIONS", "Job ID", "Stable identifier for a job or work order.", "text", "ORDER", "IDENTIFIER", "JOB", "job_id", "work_order_id", "ticket_id"),
    field("JOB_START_DATE", "OPERATIONS", "Job start date", "Date or timestamp work began.", "datetime", "ORDER", "DATE", "JOB", "job_start_date", "started_at", "start_time"),
    field("JOB_COMPLETION_DATE", "OPERATIONS", "Job completion date", "Date or timestamp work completed.", "datetime", "ORDER", "DATE", "JOB", "job_completion_date", "completed_at", "completion_time"),
    field("EMPLOYEE_ID", "OPERATIONS", "Employee ID", "Stable identifier for an employee or constrained resource.", "text", "EMPLOYEE", "IDENTIFIER", "EMPLOYEE", "employee_id", "worker_id", "technician_id", "resource_id"),
    field("EMPLOYEE_HOURS", "OPERATIONS", "Employee hours", "Paid or worked hours for an employee and period, as defined by the source.", "decimal", "EMPLOYEE", "HOURS", "EMPLOYEE", "employee_hours", "worked_hours", "labor_hours", "hours_worked"),
    field("AVAILABLE_HOURS", "OPERATIONS", "Available hours", "Capacity hours available under the represented scheduling policy.", "decimal", "EMPLOYEE", "HOURS", "EMPLOYEE", "available_hours", "capacity_hours", "scheduled_hours"),
]
