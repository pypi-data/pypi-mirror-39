# Fluentd Log Handler

Python logging handler for Fluentd

## Requirements(Python Package)

- fluent-logger

## Installation

```bash
pip install fluentd_log_handler
```

## Example

```python
import logging
from fluentd_log_handler.handler import NeilFluentdHandler

handler = NeilFluentdHandler(tag='app.worker', task_name='국민연금고지액조회')

logger = logging.getLogger('neil')
logger.addHandler(handler)

logger.error('에러 발생')
```
