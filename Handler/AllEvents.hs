{-# OPTIONS_GHC -fno-warn-orphans #-}
module Handler.AllEvents where

import Import

$(deriveJSON defaultOptions ''Event)

getAllEventsR :: Handler Value
getAllEventsR = (runDB (selectList [] []) :: Handler [Entity Event]) >>= returnJson
