from Sensor_Data_Collection.modules.L2S2Module import L2S2Module

def main():
    l2s2_module = L2S2Module("AndroidAP", "wtdm1984")
    l2s2_module.send_data("110", "6e0485b5-cd17-4438-aff8-afe0578ed71f", "4", type = 5, content = "69", units = "degrees")

if __name__ == "__main__":
    main()
