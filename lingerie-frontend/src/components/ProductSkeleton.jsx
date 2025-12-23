const ProductSkeleton = () => {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden animate-pulse">
      {/* Image skeleton */}
      <div className="aspect-square bg-gray-200"></div>

      {/* Content skeleton */}
      <div className="p-4">
        {/* Title */}
        <div className="h-4 bg-gray-200 rounded mb-2"></div>
        <div className="h-4 bg-gray-200 rounded w-3/4 mb-3"></div>

        {/* Category */}
        <div className="h-6 bg-gray-200 rounded w-20 mb-3"></div>

        {/* Price */}
        <div className="h-8 bg-gray-200 rounded w-24 mb-3"></div>

        {/* Button */}
        <div className="h-10 bg-gray-200 rounded"></div>
      </div>
    </div>
  )
}

export default ProductSkeleton
