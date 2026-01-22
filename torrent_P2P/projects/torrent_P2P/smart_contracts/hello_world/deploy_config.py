import logging
import algokit_utils

logger = logging.getLogger(__name__)

def deploy() -> None:
    from smart_contracts.artifacts.hello_world.p2_p_torrent_client import (
        P2pTorrentFactory,
        StoreFileArgs,
    )

    algorand = algokit_utils.AlgorandClient.from_environment()
    deployer = algorand.account.from_environment("DEPLOYER")

    factory = algorand.client.get_typed_app_factory(
        P2pTorrentFactory,
        default_sender=deployer.address,
    )


    app_client, result = factory.deploy(
        on_update=algokit_utils.OnUpdate.AppendApp,
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
    )

    # Funding app address (WAJIB)
    if result.operation_performed in (
        algokit_utils.OperationPerformed.Create,
        algokit_utils.OperationPerformed.Replace,
    ):
        algorand.send.payment(
            algokit_utils.PaymentParams(
                sender=deployer.address,
                receiver=app_client.app_address,
                amount=algokit_utils.AlgoAmount(algo=1),
            )
        )

    # ==== TEST CALL: store_file ====
    response = app_client.send.store_file(
        args=StoreFileArgs(
            file_hash=b"file_hash_demo",
            chunks=5,
            signature=b"peer_signature",
        )
    )

    logger.info(f"store_file result: {response.abi_return}")
    logger.info(f"APP ID = {app_client.app_id}")

