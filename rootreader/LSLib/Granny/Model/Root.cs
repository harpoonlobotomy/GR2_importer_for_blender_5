using rootreader.LSLib.Granny.GR2;

namespace rootreader.LSLib.Granny.Model;

public class Skeleton
{
    public string Name;
}
public class Mesh
{
    public string Name;
}
public class Model
{
    public string Name;
}
public class TrackGroup
{
    public string Name;
}
public class Animation
{
    public string Name;
}
public class Root
{
    public string FromFileName;
    [Serialization(Type = MemberType.ArrayOfReferences)]
    public List<Skeleton> ?Skeletons;
    [Serialization(Type = MemberType.ArrayOfReferences)]
    public List<Mesh> ?Meshes;
    [Serialization(Type = MemberType.ArrayOfReferences)]
    public List<Model> ?Models;
    [Serialization(Section = SectionType.TrackGroup, Type = MemberType.ArrayOfReferences)]
    public List<TrackGroup> ?TrackGroups;
    [Serialization(Type = MemberType.ArrayOfReferences)]
    public List<Animation> ?Animations;
    [Serialization(Kind = SerializationKind.None)]
    public uint GR2Tag;

    public static Root CreateEmpty()
    {
        return new Root
        {
            Skeletons = [],
            Meshes = [],
            Models = [],
            TrackGroups = [],
            Animations = []
        };
    }
    public void PostLoad(uint tag)
    {
        GR2Tag = tag;

        // Upgrade legacy animation formats
    }
}