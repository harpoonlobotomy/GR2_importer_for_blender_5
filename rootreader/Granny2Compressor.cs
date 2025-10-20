namespace rootreader
{
    public static class Granny2Compressor
    {
        // --- Native delegates ---
        [UnmanagedFunctionPointer(CallingConvention.StdCall)]
        private delegate bool GrannyDecompressDataProc(
            int format, bool fileIsByteReversed, int compressedBytesSize,
            IntPtr compressedBytes, int stop0, int stop1, int stop2, IntPtr decompressedBytes);

        [UnmanagedFunctionPointer(CallingConvention.StdCall)]
        private delegate IntPtr GrannyBeginFileDecompressionProc(
            int format, bool fileIsByteReversed, int decompressedBytesSize,
            IntPtr decompressedBytes, int workMemSize, IntPtr workMemBuffer);

        [UnmanagedFunctionPointer(CallingConvention.StdCall)]
        private delegate bool GrannyDecompressIncrementalProc(IntPtr state, int compressedBytesSize, IntPtr compressedBytes);

        [UnmanagedFunctionPointer(CallingConvention.StdCall)]
        private delegate bool GrannyEndFileDecompressionProc(IntPtr state);

        // --- Win32 imports ---
        [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Ansi)]
        private static extern IntPtr LoadLibrary(string lpFileName);

        [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Ansi)]
        private static extern IntPtr GetProcAddress(IntPtr hModule, string lpProcName);

        [DllImport("kernel32.dll", SetLastError = true)]
        private static extern bool FreeLibrary(IntPtr hModule);

        // --- Public methods ---
        public static byte[] Decompress(int format, byte[] compressed, int decompressedSize, int stop0, int stop1, int stop2)
        {
            IntPtr hGranny = LoadLibrary("granny2.dll");
            if (hGranny == IntPtr.Zero)
                throw new InvalidDataException("Granny2.dll is required for compressed GR2 files.");

            try
            {
                IntPtr proc = GetProcAddress(hGranny, "GrannyDecompressData");
                if (proc == IntPtr.Zero)
                    throw new InvalidDataException("GrannyDecompressData export not found in Granny2.dll.");

                var decompress = Marshal.GetDelegateForFunctionPointer<GrannyDecompressDataProc>(proc);

                byte[] decompressed = new byte[decompressedSize];
                unsafe
                {
                    fixed (byte* compPtr = compressed)
                    fixed (byte* decompPtr = decompressed)
                    {
                        bool ok = decompress(format, false, compressed.Length,
                            (IntPtr)compPtr, stop0, stop1, stop2, (IntPtr)decompPtr);
                        if (!ok)
                            throw new InvalidDataException("Failed to decompress Oodle compressed section.");
                    }
                }
                return decompressed;
            }
            finally
            {
                FreeLibrary(hGranny);
            }
        }

        public static byte[] Decompress4(byte[] compressed, int decompressedSize)
        {
            IntPtr hGranny = LoadLibrary("granny2.dll");
            if (hGranny == IntPtr.Zero)
                throw new InvalidDataException("Granny2.dll is required for compressed GR2 files.");

            try
            {
                var beginPtr = GetProcAddress(hGranny, "GrannyBeginFileDecompression");
                var incPtr = GetProcAddress(hGranny, "GrannyDecompressIncremental");
                var endPtr = GetProcAddress(hGranny, "GrannyEndFileDecompression");

                if (beginPtr == IntPtr.Zero || incPtr == IntPtr.Zero || endPtr == IntPtr.Zero)
                    throw new InvalidDataException("One or more Granny decompression exports not found in Granny2.dll.");

                var beginDecompress = Marshal.GetDelegateForFunctionPointer<GrannyBeginFileDecompressionProc>(beginPtr);
                var decompressInc = Marshal.GetDelegateForFunctionPointer<GrannyDecompressIncrementalProc>(incPtr);
                var endDecompress = Marshal.GetDelegateForFunctionPointer<GrannyEndFileDecompressionProc>(endPtr);

                byte[] decompressed = new byte[decompressedSize];
                unsafe
                {
                    fixed (byte* compPtr = compressed)
                    fixed (byte* decompPtr = decompressed)
                    {
                        IntPtr workMem = Marshal.AllocHGlobal(0x4000);
                        try
                        {
                            IntPtr state = beginDecompress(4, false, decompressedSize,
                                (IntPtr)decompPtr, 0x4000, workMem);
                            int pos = 0;
                            while (pos < compressed.Length)
                            {
                                int chunkSize = Math.Min(compressed.Length - pos, 0x2000);
                                if (!decompressInc(state, chunkSize, (IntPtr)(compPtr + pos)))
                                    throw new InvalidDataException("Failed to decompress GR2 section increment.");
                                pos += chunkSize;
                            }

                            if (!endDecompress(state))
                                throw new InvalidDataException("Failed to finish GR2 section decompression.");
                        }
                        finally
                        {
                            Marshal.FreeHGlobal(workMem);
                        }
                    }
                }
                return decompressed;
            }
            finally
            {
                FreeLibrary(hGranny);
            }
        }
    }
}
