# -*- coding: utf-8 -*-

import logging
from pymlsql.aliyun.dev.instance_context import ECSInstanceContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("build_mysql_server")

instance_context = ECSInstanceContext(keyPairName="mlsql-build-env",
                                      need_public_ip=False)
instance_context.start_server(image_id="m-bp11q5jxgj4921h8ue1h", init_ssh_key=True)

instance_context = ECSInstanceContext(keyPairName="mlsql-build-env",
                                      need_public_ip=False, instance_id="i-bp198r6ytm64r4nq86tz")
instance_context.close_server()
