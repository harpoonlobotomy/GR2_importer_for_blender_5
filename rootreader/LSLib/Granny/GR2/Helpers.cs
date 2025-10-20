using System.Linq.Expressions;

namespace rootreader.LSLib.Granny.GR2;

public static class Helpers
{
    private static readonly Dictionary<Type, ObjectCtor> CachedConstructors = [];

    public delegate object ObjectCtor();
    public delegate object ArrayCtor(int size);

    public static ObjectCtor GetConstructor(Type type)
    {
        if (!CachedConstructors.TryGetValue(type, out ObjectCtor ctor))
        {
            NewExpression newExp = Expression.New(type);
            LambdaExpression lambda = Expression.Lambda(typeof(ObjectCtor), newExp, []);
            ctor = (ObjectCtor)lambda.Compile();
            CachedConstructors.Add(type, ctor);
        }

        return ctor;
    }

    public static object CreateInstance(Type type)
    {
        ObjectCtor ctor = GetConstructor(type);
        return ctor();
    }
}