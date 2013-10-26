{-# OPTIONS_GHC -fno-warn-orphans #-}
module Handler.Event where

import Import
import Data.Maybe(fromJust)

$(deriveJSON defaultOptions ''Event)

getEventR :: EventId -> Handler Value
getEventR eId = runDB (get404 eId) >>= returnJson
