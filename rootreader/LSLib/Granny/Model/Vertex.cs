using rootreader.LSLib.Granny.GR2;

namespace rootreader.LSLib.Granny.Model;

public class Vertex
{
}

public class VertexSerializer : INodeSerializer
{
    public object Read(GR2Reader gr2, StructDefinition definition, MemberDefinition member, uint arraySize, object parent)
    {
        var vertices = new List<Vertex>((int)arraySize);
        return vertices;
    }

    public void Write(GR2Writer writer, WritableSection section, MemberDefinition member, object obj)
    {
        var items = obj as List<Vertex>;

        if (items.Count > 0)
        {
            section.StoreObjectOffset(items[0]);
        }
    }
}
