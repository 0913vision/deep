import json
import numpy as np

def S(a,b,c,n):
  return c / (1 + np.exp(-a * (n - b)))

def S_prime(a,b,c,n):
  return c * a * np.exp(-a * (n - b)) / (1 + np.exp(-a * (n - b)))**2

def L(a,b,c,n):
  return S_prime(a,b,c,b) * (n - b) + S(a,b,c,b)

def K(a,b,c,n):
  if n<=b:
    return L(a,b,c,n) / n
  return S(a,b,c,n) / n

def load_data(filename):
  with open(filename, "r", encoding="utf-8") as file:
    return json.load(file)

def constraint1(v_price, w_price, n, m, willingness):
  # print(f"{v_price},{n},{w_price},{m}, {v_price * n + w_price * m}")
  return v_price * n + w_price * m <= willingness

def constraint2(w_memory, checkpoint_size, buffer_size):
  return w_memory >= checkpoint_size * buffer_size

def NWSaturationPoint(v, w):
  bw = min(v['network_bandwidth'], w['network_bandwidth'])
  table = {
    0.3: 2,
    1.6: 10,
    5: 16,
    10: 20,
    12.5: 24,
    15: 24,
    25: 28,
    30: 32,
  }
  point = table[bw]
  return point

def constraint3(n, m, v, w):
  return n/m < NWSaturationPoint(v, w) # and n/m >= NWSaturationPoint(v, w) - 1

def FLOPP(v, type='spot'):
  # Assuming the JSON structure holds flops as a key for each instance
  if(type == 'spot'):
    spot_price = v['spot_price']
    flops = v.get('flops', 0)  # defaults to 0 if not provided
    return flops / spot_price * 3600
  else:
    ondemand_price = v['ondemand_price']
    flops = v.get('flops', 0)  # defaults to 0 if not provided
    return flops / ondemand_price * 3600

def ScalingFactor(v, n):
  a_values = {
    "g3s.xlarge": 0.1408559584,
    "g4dn.xlarge": 0.1338806402,
    "g5.xlarge": 0.08533428072
  }
  b_values = {
    "g3s.xlarge": 14.49263334,
    "g4dn.xlarge": 12.87424514,
    "g5.xlarge": 20.06669931
  }
  c_values= {
    "g3s.xlarge": 13.53250952,
    "g4dn.xlarge": 6.176666667,
    "g5.xlarge": 4.962225551
  }

  a_val = a_values[v['name']]
  b_val = b_values[v['name']]
  c_val = c_values[v['name']]

  factor = K(a_val, b_val, c_val, n)
  # if v['name'] == 'g3s.xlarge' and n==32:
  #   print("g3", factor)
  # if v['name'] == 'g4dn.xlarge' and n==32:
  #   print("g4dn", factor)
  # if v['name'] == 'g5.xlarge' and n==32:
  #   print("g5", factor)
  return factor


def findOptimalTieringArch(data, willingness, buffer_size, checkpoint_size):
  V = [instance for instance in data['instances'] if instance['type'] in ('G', 'P')]
  W = [instance for instance in data['instances'] if instance['type'] not in ('G', 'P')]

  config_list = []

  for v in V:
    for w in W:
      n_max = data['available_vcpus'][v['type']]['spot'] // v['vCPU']
      m_max = data['available_vcpus'][w['type']]['ondemand'] // w['vCPU']
        
      for n in range(1, n_max+1):
        for m in range(1, m_max+1):
          if (
            constraint1(v['spot_price'], w['ondemand_price'], n, m, willingness) and
            constraint2(w['memory'], checkpoint_size, buffer_size) and
            constraint3(n, m, v, w)
          ):
            Z = FLOPP(v) * n * ScalingFactor(v, n)
            config_list.append((Z, v, w, n, m))

  sorted_configs = sorted(config_list, key=lambda x: x[0], reverse=True)
  trimed_configs = sorted_configs[:]

  return trimed_configs


def findOptimalSingleAnchorArch(data, willingness):
  V = [instance for instance in data['instances'] if instance['type'] in ('G', 'P')]

  config_list = []

  for v in V:
    ondemand_vcpu_available = data['available_vcpus'][v['type']]['ondemand'] // v['vCPU']
    spot_vcpu_available = data['available_vcpus'][v['type']]['spot'] // v['vCPU']

    # 온디맨드 1개는 필요하므로 사용 가능한지 확인
    if ondemand_vcpu_available > 0:
      n_max = 1 + spot_vcpu_available

      for n in range(2, n_max+1):
        if v['spot_price'] * (n-1) + v['ondemand_price'] <= willingness:
          Z = (FLOPP(v) * (n-1) + FLOPP(v,'ondemand')) * ScalingFactor(v, n)
          config_list.append((Z, v, n))

  sorted_configs = sorted(config_list, key=lambda x: x[0], reverse=True)
  trimed_configs = sorted_configs[:5]

  return trimed_configs

def main():
  # Load JSON data
  data = load_data("data.json")
  
  # debugging
  # V = [instance for instance in data['instances'] if instance['type'] in ('G', 'P')]
  # for v in V:
  #   for i in [1,2,4,8,12,16,20,24,28,32]:
  #     print(f"{v['name']} | n={i} | K={ScalingFactor(v, i)}")


  # Gather user inputs
  pricing_willingness = float(input("Enter pricing willingness per hour: "))
  software = input("Enter software type (sync/async): ").strip().lower()
  
  # Determine architecture and configuration
  if software == "async":
    buffer_size = float(input("Enter buffer size: "))
    checkpoint_file_size = float(input("Enter checkpoint file size (GB): "))
    arch = "Tiering"
    config = findOptimalTieringArch(data, pricing_willingness, buffer_size, checkpoint_file_size,)
  else:
    arch = "Single Anchor"
    config = findOptimalSingleAnchorArch(data, pricing_willingness)

    # If Single Anchor does not return a valid configuration, fall back to Tiering
    if not config:
      arch = "Tiering"
      buffer_size = float(input("Enter buffer size: "))
      checkpoint_file_size = float(input("Enter checkpoint file size (GB): "))
      config = findOptimalTieringArch(data, checkpoint_file_size, buffer_size, pricing_willingness)

  # Create suggestion
  suggestion = (arch, config)
  print("===================")
  # Print suggestion
  if(arch == "Tiering"):
    for rank, cfg in enumerate(suggestion[1]):
      print(f"Rank #{rank+1}")
      print(f"Architecture: Tiering\nGPU Instance: {cfg[1]['name']}\nThe number of GPU instances: {cfg[3]}\nCPU Instance: {cfg[2]['name']}\nThe number of CPU instances: {cfg[4]}\nHourly price: {cfg[1]['spot_price'] * cfg[3] + cfg[2]['ondemand_price'] * cfg[4]}\nCFLOPP: {cfg[0]}")
      print("===================")
  else:
    for rank, cfg in enumerate(suggestion[1]):
      print(f"Rank #{rank+1}")
      print(f"Architecture: Single-anchor\nGPU Instance: {cfg[1]['name']}\nThe number of GPU instances: {cfg[2]}\nHourly price: {cfg[1]['spot_price']*(cfg[2]-1) + cfg[1]['ondemand_price']}")
      print("===================")
# print("Suggestion:", suggestion)

if __name__ == "__main__":
  main()
