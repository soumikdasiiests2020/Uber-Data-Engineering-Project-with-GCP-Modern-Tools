{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1bec98f1",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "if 'transformer' not in globals():\n",
    "    from mage_ai.data_preparation.decorators import transformer\n",
    "if 'test' not in globals():\n",
    "    from mage_ai.data_preparation.decorators import test\n",
    "\n",
    "\n",
    "@transformer\n",
    "def transform(df, *args, **kwargs):\n",
    "    \"\"\"\n",
    "    Template code for a transformer block.\n",
    "\n",
    "    Add more parameters to this function if this block has multiple parent blocks.\n",
    "    There should be one parameter for each output variable from each parent block.\n",
    "\n",
    "    Args:\n",
    "        data: The output from the upstream parent block\n",
    "        args: The output from any additional upstream blocks (if applicable)\n",
    "\n",
    "    Returns:\n",
    "        Anything (e.g. data frame, dictionary, array, int, str, etc.)\n",
    "    \"\"\"\n",
    "    # Specify your transformation logic here\n",
    "    df['trip_id'] = df.index\n",
    "    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])\n",
    "    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])\n",
    "\n",
    "    datetime_dim = df[['tpep_pickup_datetime','tpep_dropoff_datetime']].drop_duplicates().reset_index(drop=True)\n",
    "    datetime_dim['pick_hour'] = datetime_dim['tpep_pickup_datetime'].dt.hour\n",
    "    datetime_dim['pick_day'] = datetime_dim['tpep_pickup_datetime'].dt.day\n",
    "    datetime_dim['pick_month'] = datetime_dim['tpep_pickup_datetime'].dt.month\n",
    "    datetime_dim['pick_year'] = datetime_dim['tpep_pickup_datetime'].dt.year\n",
    "    datetime_dim['pick_weekday'] = datetime_dim['tpep_pickup_datetime'].dt.weekday\n",
    "\n",
    "    datetime_dim['drop_hour'] = datetime_dim['tpep_dropoff_datetime'].dt.hour\n",
    "    datetime_dim['drop_day'] = datetime_dim['tpep_dropoff_datetime'].dt.day\n",
    "    datetime_dim['drop_month'] = datetime_dim['tpep_dropoff_datetime'].dt.month\n",
    "    datetime_dim['drop_year'] = datetime_dim['tpep_dropoff_datetime'].dt.year\n",
    "    datetime_dim['drop_weekday'] = datetime_dim['tpep_dropoff_datetime'].dt.weekday\n",
    "\n",
    "    datetime_dim['datetime_id'] = datetime_dim.index\n",
    "    datetime_dim = datetime_dim[['datetime_id', 'tpep_pickup_datetime', 'pick_hour', 'pick_day', 'pick_month', 'pick_year', 'pick_weekday',\n",
    "                             'tpep_dropoff_datetime', 'drop_hour', 'drop_day', 'drop_month', 'drop_year', 'drop_weekday']]\n",
    "\n",
    "    passenger_count_dim = df[['passenger_count']].drop_duplicates().reset_index(drop=True)\n",
    "    passenger_count_dim['passenger_count_id'] = passenger_count_dim.index\n",
    "    passenger_count_dim = passenger_count_dim[['passenger_count_id','passenger_count']]\n",
    "\n",
    "    trip_distance_dim = df[['trip_distance']].drop_duplicates().reset_index(drop=True)\n",
    "    trip_distance_dim['trip_distance_id'] = trip_distance_dim.index\n",
    "    trip_distance_dim = trip_distance_dim[['trip_distance_id','trip_distance']]\n",
    "    rate_code_type = {\n",
    "        1:\"Standard rate\",\n",
    "        2:\"JFK\",\n",
    "        3:\"Newark\",\n",
    "        4:\"Nassau or Westchester\",\n",
    "        5:\"Negotiated fare\",\n",
    "        6:\"Group ride\"\n",
    "    }\n",
    "\n",
    "    rate_code_dim = df[['RatecodeID']].drop_duplicates().reset_index(drop=True)\n",
    "    rate_code_dim['rate_code_id'] = rate_code_dim.index\n",
    "    rate_code_dim['rate_code_name'] = rate_code_dim['RatecodeID'].map(rate_code_type)\n",
    "    rate_code_dim = rate_code_dim[['rate_code_id','RatecodeID','rate_code_name']]\n",
    "\n",
    "\n",
    "    pickup_location_dim = df[['pickup_longitude', 'pickup_latitude']].drop_duplicates().reset_index(drop=True)\n",
    "    pickup_location_dim['pickup_location_id'] = pickup_location_dim.index\n",
    "    pickup_location_dim = pickup_location_dim[['pickup_location_id','pickup_latitude','pickup_longitude']] \n",
    "\n",
    "\n",
    "    dropoff_location_dim = df[['dropoff_longitude', 'dropoff_latitude']].drop_duplicates().reset_index(drop=True)\n",
    "    dropoff_location_dim['dropoff_location_id'] = dropoff_location_dim.index\n",
    "    dropoff_location_dim = dropoff_location_dim[['dropoff_location_id','dropoff_latitude','dropoff_longitude']]\n",
    "\n",
    "    payment_type_name = {\n",
    "        1:\"Credit card\",\n",
    "        2:\"Cash\",\n",
    "        3:\"No charge\",\n",
    "        4:\"Dispute\",\n",
    "        5:\"Unknown\",\n",
    "        6:\"Voided trip\"\n",
    "    }\n",
    "    payment_type_dim = df[['payment_type']].drop_duplicates().reset_index(drop=True)\n",
    "    payment_type_dim['payment_type_id'] = payment_type_dim.index\n",
    "    payment_type_dim['payment_type_name'] = payment_type_dim['payment_type'].map(payment_type_name)\n",
    "    payment_type_dim = payment_type_dim[['payment_type_id','payment_type','payment_type_name']]\n",
    "\n",
    "    fact_table = df.merge(passenger_count_dim, on='passenger_count') \\\n",
    "             .merge(trip_distance_dim, on='trip_distance') \\\n",
    "             .merge(rate_code_dim, on='RatecodeID') \\\n",
    "             .merge(pickup_location_dim, on=['pickup_longitude', 'pickup_latitude']) \\\n",
    "             .merge(dropoff_location_dim, on=['dropoff_longitude', 'dropoff_latitude'])\\\n",
    "             .merge(datetime_dim, on=['tpep_pickup_datetime','tpep_dropoff_datetime']) \\\n",
    "             .merge(payment_type_dim, on='payment_type') \\\n",
    "             [['VendorID', 'datetime_id', 'passenger_count_id',\n",
    "               'trip_distance_id', 'rate_code_id', 'store_and_fwd_flag', 'pickup_location_id', 'dropoff_location_id',\n",
    "               'payment_type_id', 'fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount',\n",
    "               'improvement_surcharge', 'total_amount']]\n",
    "\n",
    "    return {\"datetime_dim\":datetime_dim.to_dict(orient=\"dict\"),\n",
    "    \"passenger_count_dim\":passenger_count_dim.to_dict(orient=\"dict\"),\n",
    "    \"trip_distance_dim\":trip_distance_dim.to_dict(orient=\"dict\"),\n",
    "    \"rate_code_dim\":rate_code_dim.to_dict(orient=\"dict\"),\n",
    "    \"pickup_location_dim\":pickup_location_dim.to_dict(orient=\"dict\"),\n",
    "    \"dropoff_location_dim\":dropoff_location_dim.to_dict(orient=\"dict\"),\n",
    "    \"payment_type_dim\":payment_type_dim.to_dict(orient=\"dict\"),\n",
    "    \"fact_table\":fact_table.to_dict(orient=\"dict\")}\n",
    "    \n",
    "\n",
    "\n",
    "@test\n",
    "def test_output(output, *args) -> None:\n",
    "    \"\"\"\n",
    "    Template code for testing the output of the block.\n",
    "    \"\"\"\n",
    "    assert output is not None, 'The output is undefined'\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.11"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
