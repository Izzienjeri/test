    def process_single_quote(self, symbol, quote):
        try:
            thread_name = threading.current_thread().name

            self.logger.log_system("info", "Processing quote",
                                   symbol=symbol,
                                   thread=thread_name,
                                   quote_details=str(quote))

            # Update latest quote
            with self.latest_quotes_lock:
                self.latest_quotes[symbol] = quote

            current_price = quote.ask_price if quote.ask_price > 0 else quote.bid_price
            current_time = quote.timestamp

            self.logger.log_analysis("info", "Quote details",
                                     symbol=symbol,
                                     ask_price=quote.ask_price,
                                     bid_price=quote.bid_price,
                                     timestamp=current_time)

            # Check existing position
            position = self.get_position(symbol)
            if position is not None:
                with self.trading_levels_lock:
                    levels = self.trading_levels.get(symbol)

                if levels is not None:
                    nearest_level = self.find_nearest_level(levels, current_price)
                    if nearest_level is not None:
                        level_price = nearest_level['level']

                        if abs(current_price - level_price) <= self.level_threshold:
                            self.logger.log_analysis("info", "Price at key level",
                                                     symbol=symbol,
                                                     price=current_price,
                                                     level=level_price)

                            latest_data = self.get_latest_data_points(symbol)
                            if latest_data is not None:
                                signal, signal_price = self.generate_signals(
                                    symbol, current_price, latest_data, level_price, 2
                                )

                                if signal != 0:
                                    qty = float(position.qty)
                                    if (qty > 0 and signal < 0) or (qty < 0 and signal > 0):
                                        self.logger.log_trade("info", "Closing position on fractal analysis",
                                                              symbol=symbol,
                                                              signal=signal,
                                                              position_qty=qty)
                                        self.alpaca.close_position(symbol)
            else:
                self.check_and_place_orders(symbol)

        except Exception as e:
            self.logger.log_error("system", f"Quote processing error for {symbol}", exc_info=True)

# here is find nearest level
    def find_nearest_level(self, levels_df, current_price):
        """Find the nearest support/resistance level to the current price"""
        try:
            recent_levels = levels_df.iloc[-1]
            level_price = recent_levels['level']
            level_type = recent_levels['level_type']

            return {
                'level': level_price,
                'type': level_type
            }
        except Exception as e:
            self.logger.log_error("analysis", "Error finding nearest level", exc_info=True)
            return None
