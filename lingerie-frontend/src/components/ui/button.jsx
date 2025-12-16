import React from 'react'

export const Button = ({
  children,
  className = '',
  size = 'md',
  variant = 'default',
  onClick,
  ...props
}) => {
  const sizeClasses = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg'
  }

  const variantClasses = {
    default: 'bg-pink-600 hover:bg-pink-700 text-white',
    outline: 'border-2 border-pink-600 text-pink-600 hover:bg-pink-50',
    ghost: 'hover:bg-gray-100 text-gray-700'
  }

  return (
    <button
      className={`
        inline-flex items-center justify-center
        font-medium rounded-lg
        transition-colors duration-200
        focus:outline-none focus:ring-2 focus:ring-pink-600 focus:ring-offset-2
        disabled:opacity-50 disabled:cursor-not-allowed
        ${sizeClasses[size]}
        ${variantClasses[variant]}
        ${className}
      `}
      onClick={onClick}
      {...props}
    >
      {children}
    </button>
  )
}
