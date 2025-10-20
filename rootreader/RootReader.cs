using Newtonsoft.Json;

// based on lslib-master\LSLib\Granny\GR2Utils.cs and uses modified versions of Reader.CS, Root.cs and associated scripts. //

// this one is mostly chatgpt. I've never written C++. Cannot speak to the quality of it. //

using rootreader.LSLib.Granny.GR2;
using rootreader.LSLib.Granny.Model;

namespace rootreader
{
    class RootReader
    {
        static int Main(string[] args)
        {
            if (args.Length == 0)
            {
                //Console.Error.WriteLine("Usage: RootReader.exe <inputFilePath>");
                //return 1; // TRIGGERS ERROR (0x01) IF ENABLED. IF HARDCODING ARGS, TURN OFF. IF USING REAL ARGS, TURN ON.

                args = ["F:\\test\\gltf_tests\\randompeaceintdev defaults copyskel.gr2"];
                //Console.WriteLine("Using hardcoded GR2 filepath");
                //args = new[] { "F:\\BG3 Extract PAKs\\PAKs\\Models\\Generated\\Public\\Shared\\Assets\\Characters\\_Models\\_Creatures\\Intellect_Devourer\\Resources\\INTDEV_CIN.GR2" };
                //args = new[] { "F:\\BG3 Extract PAKs\\PAKs\\Models\\Public\\Shared\\Assets\\Characters\\_Anims\\_Creatures\\Intellect_Devourer\\INTDEV_Rig\\INTDEV_Rig_DFLT_IDLE_Random_Peace_01.GR2" };
            }

            string inputPath = args[0];

            try
            {
                // Open the GR2 file
                using var fs = File.Open(inputPath, FileMode.Open, FileAccess.Read, FileShare.ReadWrite);

                // Create a Root object
                var root = new Root();

                // Read GR2 into root
                var gr2 = new GR2Reader(fs);
                gr2.Read(root);

                // Post-load processing
                root.PostLoad(gr2.Tag);

                // Serialize to JSON
                string json = JsonConvert.SerializeObject(root, Formatting.Indented);
                //string json = JsonSerializer.Serialize(root, Formatting.Indented);

                //  "Skeletons": null,
                //  "Meshes": null,
                //  "Models": null,
                //  "TrackGroups": null,
                //  "Animations": null,
                //  "GR2Tag": 2147483705

                // Print JSON to stdout
                Console.WriteLine(json);

                // ...
                return 0;
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine("Error: " + ex.Message);
                return 2;
            }
        }
    }
}