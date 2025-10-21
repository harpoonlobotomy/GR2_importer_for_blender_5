using rootreader.LSLib.Granny.GR2;
using rootreader.LSLib.LS;
using System.Xml;
using System.Text.RegularExpressions;
using System.Xml.Linq;
using rootreader.LSLib.Granny.Model;
using rootreader.LSLib.Granny;

namespace LSLib.Granny.Model;


public class ColladaExporter
{
    [Serialization(Kind = SerializationKind.None)]
    private XmlDocument Xml = new();

    private Game DetectGame(Root root)
    {
        if (root.GR2Tag == Header.Tag_DOS)
        {
            return Game.DivinityOriginalSin;
        }

        if (root.GR2Tag == Header.Tag_DOS2DE)
        {
            return Game.DivinityOriginalSin2DE;
        }

        if (root.GR2Tag == Header.Tag_DOSEE)
        {
            return Game.BaldursGate3;
        }

        return Game.Unset;
    }

    private technique ExportRootLSLibProfile(Root root)
    {
        var profile = new technique()
        {
            profile = "LSTools"
        };

        var props = new List<XmlElement>();

        var prop = Xml.CreateElement("LSLibMajor");
        prop.InnerText = Common.MajorVersion.ToString();
        props.Add(prop);

        prop = Xml.CreateElement("LSLibMinor");
        prop.InnerText = Common.MinorVersion.ToString();
        props.Add(prop);

        prop = Xml.CreateElement("LSLibPatch");
        prop.InnerText = Common.PatchVersion.ToString();
        props.Add(prop);

        prop = Xml.CreateElement("MetadataVersion");
        prop.InnerText = Common.ColladaMetadataVersion.ToString();
        props.Add(prop);

        var game = DetectGame(root);
        if (game != Game.Unset)
        {
            prop = Xml.CreateElement("Game");
            prop.InnerText = game.ToString();
            props.Add(prop);
        }

        profile.Any = props.ToArray();
        return profile;
    }

    public void Export(Root root, string outputPath)
    {
        var asset = new asset
        {
            created = DateTime.Now,
            modified = DateTime.Now,
            unit = new assetUnit
            {
                name = "meter"
            },
            up_axis = UpAxisType.Y_UP
        };
                var rootElements = new List<object>();
        var visualScenes = new library_visual_scenes();
        var visualScene = new visual_scene
        {
            id = "DefaultVisualScene",
            name = "unnamed",
        };
        visualScenes.visual_scene = [visualScene];

        var visualSceneInstance = new InstanceWithExtra
        {
            url = "#DefaultVisualScene"
        };
        rootElements.Add(visualScenes);

        var scene = new COLLADAScene
        {
            instance_visual_scene = visualSceneInstance
        };

        var collada = new COLLADA
        {
            asset = asset,
            scene = scene,
            Items = rootElements.ToArray(),
            extra =
            [
                new extra
                {
                    technique =
                    [
                        ExportRootLSLibProfile(root)
                    ]
                }
            ]
        };

        using var stream = File.Open(outputPath, FileMode.Create);
        collada.Save(stream);
    }
}
