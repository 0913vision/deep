import json

def load_data(filename):
  with open(filename, "r", encoding="utf-8") as file:
    return json.load(file)

def constraint1(v_price, w_price, n, m, willingness):
  # print(f"{v_price},{n},{w_price},{m}, {v_price * n + w_price * m}")
  return v_price * n + w_price * m <= willingness

def constraint2(w_memory, checkpoint_size, buffer_size):
  return w_memory >= checkpoint_size * buffer_size

def NWSaturationPoint(v, w):
  # Placeholder. Actual logic will be implemented later.
  return 0

def constraint3(n, m, v, w):
  return n/m > NWSaturationPoint(v, w)

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
  # Placeholder. Actual logic will be implemented later.
  return 1


def findOptimalTieringArch(data, willingness, buffer_size, checkpoint_size):
  V = [instance for instance in data['instances'] if instance['type'] in ('G', 'P')]
  W = [instance for instance in data['instances'] if instance['type'] not in ('G', 'P')]

  Z_max = 0
  optimal_config = None

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
            if Z > Z_max:
              Z_max = Z
              optimal_config = (v, w, n, m)

  return optimal_config


def findOptimalSingleAnchorArch(data, willingness):
  V = [instance for instance in data['instances'] if instance['type'] in ('G', 'P')]

  z_max = 0
  optimal_config = None

  for v in V:
    ondemand_vcpu_available = data['available_vcpus'][v['type']]['ondemand'] // v['vCPU']
    spot_vcpu_available = data['available_vcpus'][v['type']]['spot'] // v['vCPU']

    # 온디맨드 1개는 필요하므로 사용 가능한지 확인
    if ondemand_vcpu_available > 0:
      n_max = 1 + spot_vcpu_available

      for n in range(2, n_max+1):
        if v['spot_price'] * (n-1) + v['ondemand_price'] <= willingness:
          Z = (FLOPP(v) * (n-1) + FLOPP(v,'ondemand')) * ScalingFactor(v, n)
          if Z > z_max:
            z_max = Z
            optimal_config = (v, n)

  return optimal_config

def main():
  # Load JSON data
  data = load_data("data.json")
  
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
  
  # Print suggestion
  if(arch == "Tiering"):
    print("===================")
    print(f"Architecture: {suggestion[0]}\nGPU Instance: {suggestion[1][0]['name']}\nThe number of GPU instances: {suggestion[1][2]}\nCPU Instance: {suggestion[1][1]['name']}\nThe number of CPU instances: {suggestion[1][3]}\nHourly price: {suggestion[1][0]['spot_price'] * suggestion[1][2] + suggestion[1][1]['ondemand_price'] * suggestion[1][3]}")
    print("===================")
  else:
    print("===================")
    print(f"Architecture: {suggestion[0]}\nGPU Instance: {suggestion[1][0]['name']}\nThe number of GPU instances: {suggestion[1][1]}\nHourly price: {suggestion[1][0]['spot_price']*(suggestion[1][1]-1) + suggestion[1][0]['ondemand_price']}")
    print("===================")
  # print("Suggestion:", suggestion)

if __name__ == "__main__":
  main()
