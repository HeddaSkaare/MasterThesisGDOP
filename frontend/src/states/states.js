import { atom } from 'jotai'

export const updateDataState = atom(false)

export const timeState = atom(new Date(new Date().toISOString().slice(0, 16) + ":00.000Z"))

export const epochState = atom(0)

export const elevationState = atom(10)

export const gnssState = atom({
    GPS: true,
    GLONASS: true,
    Galileo: true,
    BeiDou: true,
    QZSS: true,
    NavIC: true,
    SBAS:true,
  })
