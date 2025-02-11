### very quick:
```
sudo kubeadm init --pod-network-cidr=10.200.0.0/16,2001:db8:200:0::/56 --service-cidr=10.96.0.0/20,2001:db8:44:44:44:44::/112
helm install cilium isovalent/cilium --version 1.15.6  --namespace kube-system -f helm-cilium-ent.yaml
helm get values cilium -n kube-system
kubectl taint nodes --all node-role.kubernetes.io/control-plane-
kubectl apply -f bgp-cp.yaml 
kubectl apply -f bgp-wkr.yaml
cilium bgp peers
kubectl apply -f locator-pool.yaml 
kubectl get sidmanager -o yaml
kubectl get IsovalentSRv6EgressPolicy -o yaml
kubectl apply -f vrf-blue.yaml 
kubectl create namespace blue
kubectl apply -f nginx-blue.yaml 

kubectl exec -it -n kube-system cilium-22mvq -- cilium-dbg bpf srv6 policy
kubectl exec -it -n kube-system cilium-22mvq -- cilium-dbg bpf srv6 sid
kubectl exec -it -n kube-system cilium-22mvq -- cilium-dbg bpf srv6 vrf
cilium bgp routes advertised ipv4 mpls_vpn

kubectl annotate --overwrite nodes k8s-cp-node00 cilium.io/bgp-virtual-router.65044="router-id=10.44.1.2,srv6-responder=true"
kubectl get IsovalentSRv6EgressPolicy -o yaml
```


table reference

### Virtual Machine Access Table
| VM Name        | Description                    | Access Type |   IP Address    |
|:---------------|:-------------------------------|:-----------:|:---------------:|
| topology-host  | Ubuntu, Containerlab, XRds     | SSH         | 198.18.133.100  |
| k8s-cp-node00  | Ubuntu k8s control plane node  | SSH         | 198.18.133.106  |
| k8s-wkr-node01 | Ubuntu k8s worker node         | SSH         | 198.18.133.107  |