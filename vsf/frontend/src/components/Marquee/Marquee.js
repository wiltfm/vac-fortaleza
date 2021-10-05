import './marquee.css'
import React, { useEffect, useState } from 'react'

export default function Marquee({ children }) {
    return (
        <p className="marquee"> <span>{children} </span> </p>
    )
}
