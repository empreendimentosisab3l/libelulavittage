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
    default: 'bg-[#c9a96e] hover:bg-[#b8986e] text-black font-semibold',
    outline: 'border-2 border-[#c9a96e] text-[#c9a96e] hover:bg-[#c9a96e]/10',
    ghost: 'hover:bg-[#1a1a1a] text-white'
  }

  return (
    <button
      className={`
        inline-flex items-center justify-center
        font-medium rounded-lg
        transition-colors duration-200
        focus:outline-none focus:ring-2 focus:ring-[#c9a96e] focus:ring-offset-2 focus:ring-offset-[#0a0a0a]
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
