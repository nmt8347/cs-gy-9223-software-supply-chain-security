import argparse
from util import extract_public_key, verify_artifact_signature
from merkle_proof import (
    DefaultHasher,
    verify_consistency,
    verify_inclusion,
    compute_leaf_hash,
)
import requests
import json
import base64
import os


# Problem 1
def validate_log_index(log_index):
    """
    Validate that the log index is a non-negative integer.
    """
    try:
        test_if_int = int(log_index)
        if test_if_int < 0:
            raise ValueError("log index  must be a non-negative integer")
    except ValueError:
        return False
    return True


# Problem 1
def get_log_entry(log_index, debug=False):
    """
    Fetch entry details from Rekor for a given log index.
    """
    # Check if log_index is a non-negative integer (sane value)
    if not validate_log_index(log_index):
        return None

    # Use v1 API endpoint to fetch log entry details
    REKOR_LOG_ENTRIES_URL = "https://rekor.sigstore.dev/api/v1/log/entries"
    response = requests.get(
        REKOR_LOG_ENTRIES_URL, params={"logIndex": log_index}, timeout=30
    )
    if response.status_code != 200:
        print(f"Error fetching log entry for index {log_index}")
        return None

    # Get base64 encoded log entry from response
    log_entry = response.json()

    # Debug: Print the log entry details if debug mode is enabled
    if debug:
        print(f"Log entry for index {log_index}:")
        print(json.dumps(log_entry, indent=4), end="\n")

    # Return the log entry details
    for _, data in log_entry.items():
        return data
    return None


# Problem 1
def get_verification_proof(log_index, debug=False):
    """
    Get the verification proof for a given log index from Rekor.
    """
    log_entry = get_log_entry(log_index, debug)
    if log_entry is None:
        print(f"Error: no log entry returned for index {log_index}")
        return None

    # Get the inclusion proof from the log entry's verification details
    verification_proof = log_entry["verification"]
    inclusion_proof = verification_proof["inclusionProof"]

    # Return the inclusion proof details along with the computed leaf hash
    return {
        "index": inclusion_proof["logIndex"],
        "tree_size": inclusion_proof["treeSize"],
        "hashes": inclusion_proof["hashes"],
        "root_hash": inclusion_proof["rootHash"],
        "leaf_hash": compute_leaf_hash(log_entry["body"]),
    }


# Problem 1
def inclusion(log_index, artifact_filepath, debug=False):
    if not os.path.isfile(artifact_filepath):
        print(f"Artifact file '{artifact_filepath}' does not exist.")
        return

    log_entry = get_log_entry(log_index, debug)

    # Extract "body" from the log entry, which is base64 encoded
    body = log_entry["body"]
    body_decoded = base64.b64decode(body)  # .decode('utf-8')
    body_json = json.loads(body_decoded)

    # Extract signature and certificate from the body
    signature = base64.b64decode(body_json["spec"]["signature"]["content"])
    certificate = base64.b64decode(
        body_json["spec"]["signature"]["publicKey"]["content"]
    )

    # Extract public key from the certificate
    public_key = extract_public_key(certificate)

    # Verify the artifact signature using the extracted public key
    verify_artifact_signature(signature, public_key, artifact_filepath)

    # Get the verification proof for the log index
    proof = get_verification_proof(log_index, debug)
    index = proof["index"]
    tree_size = proof["tree_size"]
    leaf_hash = proof["leaf_hash"]
    hashes = proof["hashes"]
    root_hash = proof["root_hash"]

    # Verify inclusion for a given log index with the proof key-value pairs
    verify_inclusion(DefaultHasher, index, tree_size, leaf_hash, hashes, root_hash)

    print(
        f"Successfully verified inclusion of log index {log_index} "
        f"for artifact '{artifact_filepath}'."
    )


# Problem 2
def get_latest_checkpoint(debug=False):
    """
    Fetch the latest checkpoint from Rekor.
    """
    REKOR_CHECKPOINT_URL = "https://rekor.sigstore.dev/api/v1/log/"
    response = requests.get(REKOR_CHECKPOINT_URL, timeout=30)
    if response.status_code != 200:
        print("Error fetching latest checkpoint from Rekor")
        return None

    # Get the latest checkpoint from the response
    latest_checkpoint = response.json()

    # Debug: Print the latest checkpoint details if debug mode is enabled
    if debug:
        print("Latest checkpoint from Rekor:")
        print(json.dumps(latest_checkpoint, indent=4), end="\n")

        # Store the latest checkpoint in a file for debugging purposes
        with open("checkpoint.json", "w") as f:
            json.dump(latest_checkpoint, f, indent=4)

    return latest_checkpoint


# Problem 2
def consistency(prev_checkpoint, debug=False):
    # TODO:
    # verify that prev checkpoint is not empty
    # get_latest_checkpoint()
    """
    Verify consistency of the transparency log.
    """
    # Verify that the previous checkpoint is not empty and
    # contains the treeID, treeSize, and rootHash keys
    for k in ["treeID", "treeSize", "rootHash"]:
        if k not in prev_checkpoint:
            print(f"Error missing key of previous checkpoint: {k}")
            return

    # Fetch the latest checkpoint from Rekor
    latest_checkpoint = get_latest_checkpoint(debug)
    if latest_checkpoint is None:
        return
    if debug:
        print("Latest checkpoint:")
        print(latest_checkpoint, end="\n\n")

    tree_id = prev_checkpoint["treeID"]
    prev_size, prev_root_hash = (
        prev_checkpoint["treeSize"],
        prev_checkpoint["rootHash"],
    )  # older hash
    latest_size, latest_root_hash = (
        latest_checkpoint["treeSize"],
        latest_checkpoint["rootHash"],
    )  # latest hash

    if debug:
        print(
            f"{prev_size=}\n{latest_size=}\n{prev_root_hash=}\n{latest_root_hash=}",
            end="\n\n",
        )

    # Ensure that the tree sizes are valid and that the tree ID matches
    # between the previous and latest checkpoints.
    # The first size must be at least 1,
    # and the second size must be greater than or equal to the first size.
    if prev_size < 1 or latest_size < prev_size:
        print(f"Error: invalid tree sizes given: [{prev_size}, {latest_size}]")
        return
    if str(tree_id) != str(latest_checkpoint["treeID"]):
        print(f"Error: tree ID mismatch: {tree_id} vs {latest_checkpoint['treeID']}")
        return

    # Get the consistency proof
    # Equal sizes do not require proof
    proof = []
    if prev_size != latest_size:
        REKOR_LOG_PROOF_URL = "https://rekor.sigstore.dev/api/v1/log/proof"
        response = requests.get(
            REKOR_LOG_PROOF_URL,
            params={
                "firstSize": prev_size,
                "lastSize": latest_size,
                "treeID": tree_id,
            },
            timeout=30,
        )
        response.raise_for_status()  # Catch any HTTP errors (4xx/5xx)
        proof = response.json()["hashes"]
    if debug:
        print("Proof:")
        print(proof, end="\n\n")

    # Verify the user's checkpoint is consistent with the latest checkpoint
    try:
        verify_consistency(
            DefaultHasher,
            prev_size,
            latest_size,
            proof,
            prev_root_hash,
            latest_root_hash,
        )
    except ValueError as e:
        print(f"Consistency verification failed: {e}")
        return

    print("Consistency verification successful.")


def main():
    debug = False
    parser = argparse.ArgumentParser(description="Rekor Verifier")
    parser.add_argument(
        "-d", "--debug", help="Debug mode", required=False, action="store_true"
    )  # Default false
    parser.add_argument(
        "-c",
        "--checkpoint",
        help="Obtain latest checkpoint\
                        from Rekor Server public instance",
        required=False,
        action="store_true",
    )
    parser.add_argument("--inclusion", help="Verify inclusion of an\
                        entry in the Rekor Transparency Log using log index\
                        and artifact filename.\
                        Usage: --inclusion 126574567", required=False, type=int)
    parser.add_argument("--artifact", help="Artifact filepath for verifying\
                        signature", required=False)
    parser.add_argument("--consistency", help="Verify consistency of a given\
                        checkpoint with the latest checkpoint.", action="store_true")
    parser.add_argument(
        "--tree-id", help="Tree ID for consistency proof", required=False
    )
    parser.add_argument(
        "--tree-size", help="Tree size for consistency proof", required=False, type=int
    )
    parser.add_argument(
        "--root-hash", help="Root hash for consistency proof", required=False
    )
    args = parser.parse_args()
    if args.debug:
        debug = True
        print("enabled debug mode")
    if args.checkpoint:
        # get and print latest checkpoint from server
        # if debug is enabled, store it in a file checkpoint.json
        checkpoint = get_latest_checkpoint(debug)
        print(json.dumps(checkpoint, indent=4))
    if args.inclusion:
        inclusion(args.inclusion, args.artifact, debug)
    if args.consistency:
        if not args.tree_id:
            print("please specify tree id for prev checkpoint")
            return
        if not args.tree_size:
            print("please specify tree size for prev checkpoint")
            return
        if not args.root_hash:
            print("please specify root hash for prev checkpoint")
            return

        prev_checkpoint = {}
        prev_checkpoint["treeID"] = args.tree_id
        prev_checkpoint["treeSize"] = args.tree_size
        prev_checkpoint["rootHash"] = args.root_hash

        consistency(prev_checkpoint, debug)


if __name__ == "__main__":
    main()
