import sys
from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-01-3c21c96f2321"

def seed_firestore():
    print(f"Connecting to Firestore for project: {PROJECT_ID}...")
    db = firestore.Client(project=PROJECT_ID)

    guides = [
        {
            "title": "No Internet Connection",
            "category": "Networking",
            "symptoms": "Unable to reach external websites or ping public IP addresses.",
            "solution": "Check physical cable or Wi-Fi connection, verify local IP assignment via DHCP, and restart the network interface or router.",
            "commands": "ip a, ping 8.8.8.8, systemctl restart NetworkManager"
        },
        {
            "title": "DNS Name Resolution Failure",
            "category": "Networking",
            "symptoms": "Can ping IP addresses directly (e.g., 8.8.8.8), but domain names fail to resolve (e.g., google.com).",
            "solution": "Check your /etc/resolv.conf file for valid nameservers (like 8.8.8.8 or 1.1.1.1) and flush local DNS cache.",
            "commands": "nslookup google.com, dig google.com, cat /etc/resolv.conf"
        },
        {
            "title": "Linux Permission Denied Error",
            "category": "Linux",
            "symptoms": "Error message 'Permission denied' when executing a script or accessing a file.",
            "solution": "Verify file ownership and permission modes. Grant execution permissions with chmod +x or execute with appropriate sudo privileges.",
            "commands": "ls -l <file>, chmod +x <script>, sudo <command>"
        },
        {
            "title": "AWS IAM AccessDenied Error",
            "category": "AWS",
            "symptoms": "AWS CLI or SDK call fails with 'AccessDenied' or 'UnauthorizedOperation'.",
            "solution": "Check IAM policy attached to the user/role for missing permissions. Verify correct AWS credentials and active profile.",
            "commands": "aws sts get-caller-identity, aws iam list-attached-user-policies"
        },
        {
            "title": "Basic Network Connectivity Troubleshooting",
            "category": "Networking",
            "symptoms": "Intermittent packet loss or high latency to remote host.",
            "solution": "Trace the network path to find hop failures, check interface stats for error packets, and verify MTU size.",
            "commands": "traceroute <host>, mtr <host>, netstat -i"
        }
    ]

    collection_ref = db.collection("troubleshooting_guides")
    for guide in guides:
        doc_ref = collection_ref.document()
        doc_ref.set(guide)
        print(f"Added guide: '{guide['title']}' with ID: {doc_ref.id}")

    print("Successfully seeded troubleshooting_guides collection!")

if __name__ == "__main__":
    seed_firestore()
