const ProductSkeleton = () => {
  return (
    <div className="bg-[#1a1a1a] rounded-lg shadow-md overflow-hidden animate-pulse border border-[#c9a96e]/10">
      {/* Image skeleton */}
      <div className="aspect-square bg-[#0a0a0a]"></div>

      {/* Content skeleton */}
      <div className="p-4">
        {/* Title */}
        <div className="h-4 bg-[#0a0a0a] rounded mb-2"></div>
        <div className="h-4 bg-[#0a0a0a] rounded w-3/4 mb-3"></div>

        {/* Category */}
        <div className="h-6 bg-[#0a0a0a] rounded w-20 mb-3"></div>

        {/* Price */}
        <div className="h-8 bg-[#0a0a0a] rounded w-24 mb-3"></div>

        {/* Button */}
        <div className="h-10 bg-[#c9a96e]/20 rounded"></div>
      </div>
    </div>
  )
}

export default ProductSkeleton
