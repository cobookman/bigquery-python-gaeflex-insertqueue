# Copyright 2017 Google Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import threading
import logging
import time

from google.cloud import bigquery
from queue import Queue
from queue import Empty

client = bigquery.Client()
row_queue = Queue()
is_running = False
is_stopped = True

def async_insert_row(row):
  """adds row to queue to be inserted."""
  global row_queue
  row_queue.put(row)
  print("There are now ", row_queue.qsize(), " rows queued up")


def stop():
  """Stops the background bq service."""
  global is_running
  global is_stopped

  is_running = False

  # Block until service stopped.
  while is_stopped == False:
    pass

def start(dataset_name, table_name):
  """Starts the background bq service."""
  global is_running
  global client
  global dataset
  global table

  if is_running:
    return

  print("Starting up background bq service.")
  print("\tConnecting to BQ")
  dataset = client.dataset(dataset_name)
  table = dataset.table(table_name)
  table.reload()

  print("\tStarting up thread")
  is_running = True
  thread = threading.Thread(target=run, args=())
  thread.start()
  return thread


def _get_n_from_queue(n):
    """Grabs up to n items from queue."""
    global row_queue

    items = []
    for i in range(0, n):
      try:
        item = row_queue.get_nowait()
        items.append(item)
      except Empty:
        break
    return items


def run():
  """Background process for inserting items into BQ."""
  global is_stopped
  global is_running
  global table

  is_stopped = False
  while is_running:
    time.sleep(3)
    print("Running, grabbing rows")

    # Grab up to 100 items at a time
    rows = _get_n_from_queue(100)
    if len(rows) > 0:
      print("Got rows: ", rows)

      # Insert rows into bq
      errors = table.insert_data(rows)
      if errors:
        print("Errors: ", errors)
      else:
        print("Inserted rows: ", rows)

    is_stopped = True

