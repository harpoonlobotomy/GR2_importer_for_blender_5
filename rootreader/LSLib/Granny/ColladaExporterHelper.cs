using rootreader.LSLib.Granny.GR2;
using rootreader.LSLib.Granny.Model;
using rootreader.LSLib.LS;
using System;
using System.Linq.Expressions;
using System.Xml;

namespace rootreader.LSLib.Granny;

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

            return Game.BaldursGate3;
        }

    private technique ExportRootLSLibProfile(Stream stream)
        {
            var profile = new technique()
            {
                profile = "LSTools"
            };

            var props = new List<XmlElement>();

            //var prop = Xml.CreateElement("LSLibMajor");
            //prop.InnerText = Common.MajorVersion.ToString();
           // props.Add(prop);

           // prop = Xml.CreateElement("LSLibMinor");
           // prop.InnerText = Common.MinorVersion.ToString();
           // props.Add(prop);

          //  prop = Xml.CreateElement("LSLibPatch");
           // prop.InnerText = Common.PatchVersion.ToString();
          //  props.Add(prop);

           // prop = Xml.CreateElement("MetadataVersion");
           // prop.InnerText = Common.ColladaMetadataVersion.ToString();
           // props.Add(prop);

            var game = DetectGame(gr2);
            if (game != null) // changed from games.unset from the enums to null for testing.
            {
                var prop = Xml.CreateElement("Game");
                prop.InnerText = game.ToString();
                props.Add(prop);
            }

            profile.Any = props.ToArray();
            return profile;
        }

