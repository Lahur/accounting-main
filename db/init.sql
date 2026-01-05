CREATE TABLE IF NOT EXISTS outgoing_recipient (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    postal_code TEXT NOT NULL,
    city TEXT NOT NULL,
    oib TEXT NOT NULL,
    modified TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS outgoing_bill (
    id UUID PRIMARY KEY,
    project_name TEXT NOT NULL,
    project_description TEXT NOT NULL,
    base_price DECIMAL NOT NULL,
    pdv_price DECIMAL NOT NULL,
    price DECIMAL NOT NULL,
    price_text TEXT NOT NULL,
    date_time TIMESTAMP WITH TIME ZONE NOT NULL,
    recipient_id UUID NOT NULL,
    bill_number BIGINT NOT NULL UNIQUE,
    modified TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recipient_id) REFERENCES outgoing_recipient(id)
);