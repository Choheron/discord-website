"use client"

import Snowfall from "react-snowfall"

export default function ClientSnowfall(props) {
  return(
    <Snowfall
      style={{
        position: 'fixed',
        width: '100vw',
        height: '100vh',
      }}
    />
  )
}